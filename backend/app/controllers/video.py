import asyncio
from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService
from third_party.cloudinary import CloudinaryService
from fastapi import HTTPException
import os
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from models.video import Video

class VideoController:
    @staticmethod
    async def create_video(db: AsyncSession, topic: str, email: str, user_id: int, language_code: str = "en-US"):
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        try:
            subtitles_service = SubtitlesService(topic=topic, language_code=language_code)
            subtitles = await subtitles_service.generate_subtitles()
            
            audio_service = AudioService()
            image_service = ImageService()
            
            audio_urls, image_urls = await asyncio.gather(
                audio_service.generate_audio(subtitles=subtitles, language_code=language_code, email=email),
                image_service.generate_image(subtitles=subtitles, email=email)
            )
            
            video_service = VideoService(
                image_urls=image_urls,
                audio_urls=audio_urls,
                subtitles=subtitles,
                email=email
            )
            result = await video_service.create_video()
            
            # Save video metadata to database
            video_data = result.copy()
            
            # Upload image and audio files to Cloudinary
            cloudinary_service = CloudinaryService()
            upload_image_tasks = []
            upload_audio_tasks = []

            for i in range(len(image_urls)):
                image_path = f'public/images/{email}-output{i}.jpg'
                audio_path = f'public/audios/{email}-output{i}.mp3'
                
                # Append tasks to the list
                upload_image_tasks.append(cloudinary_service.upload_image(image_path))
                upload_audio_tasks.append(cloudinary_service.upload_audio(audio_path))

            # Run all image and audio uploads concurrently
            image_results, audio_results = await asyncio.gather(
                asyncio.gather(*upload_image_tasks),
                asyncio.gather(*upload_audio_tasks)
            )

            # Add results to video_data
            video_data['image_urls'] = image_results
            video_data['audio_urls'] = audio_results
            video_data['topic'] = topic
            video_data['subtitles'] = subtitles
            
            # Create video record in the database
            await Video.create(db, user_id=user_id, video_data=video_data)
            
            #delete files after video creation
            for i in range(len(image_urls)):
                image_path = f'public/images/{email}-output{i}.jpg'
                audio_path = f'public/audios/{email}-output{i}.mp3'
                if os.path.exists(image_path):
                    os.remove(image_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            
        except Exception as e:
            print(f"Error creating video: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate video")
        
        return result, 200
    
    
    @staticmethod
    async def update_video(db: AsyncSession, email: str, video_id: int, text_effect: str=None, music: str=None, stickers: str=None):
        video = await Video.get_by_id(db, video_id)
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        try:    
            #update video
            video_service = VideoService(
                image_urls=video.image_urls,
                audio_urls=video.audio_urls,
                subtitles=video.subtitles,
                email= email
            )
            
            result = await video_service.create_video(
                text_effect=text_effect,
                music=music,
                stickers=stickers
            )
            
            # delete old video from Cloudinary
            cloudinary_service = CloudinaryService()
            cloudinary_service.delete_file(video.video)
            
            video.video = result['video']
            if text_effect is not None:
                video.text_effect = text_effect
            if music is not None:
                video.music = music
            if stickers is not None:
                video.stickers = stickers
            
            await db.commit()
            await db.refresh(video)
            
        except Exception as e:
            print(f"Error updating video: {e}")
            raise HTTPException(status_code=500, detail="Failed to update video")
        
        return result, 200
    
    
    @staticmethod
    async def get_video(db: AsyncSession, video_id: int):
        try:
            video = await Video.get_by_id(db, video_id)
            return video, 200
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Video not found")
        except Exception as e:
            print(f"Error fetching video: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch video")
        
    
    