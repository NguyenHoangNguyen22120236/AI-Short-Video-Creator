import asyncio
from collections import defaultdict
from app.services.subtitles import SubtitlesService
from app.services.audio import AudioService
from app.services.image import ImageService
from app.services.video import VideoService
from app.third_party.cloudinary import CloudinaryService
from app.models.video import Video
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
import os

class VideoController:
    @staticmethod
    async def create_video(db: AsyncSession, topic: str, email: str, user_id: int, language_code: str = "en-US"):
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        try:
            subtitles_service = SubtitlesService(topic=topic, language_code=language_code)
            subtitles = await subtitles_service.generate_subtitles()
            print(f"Generated subtitles: {subtitles}")
            
            #subtitles=['Những con phố Hà Nội khoác lên mình làn sương mỏng như tơ, mặt hồ Gươm lặng in bóng những hàng liễu rủ. Tiếng leng keng xe đạp hòa cùng mùi cốm non thoảng nhẹ trong gió.', 'Nắng thu vàng óng trải dài trên mặt hồ Tây, soi bóng những quán cà phê nhỏ. Người dân thong thả nhấp chén trà nóng, lắng nghe tiếng lá xào xạc rơi bên thềm.', 'Những đứa trẻ nô đùa trên hè phố, tung tăng đuổi theo chiếc lá bàng đỏ thắm. Mùi hoa sữa nồng nàn phả vào không gian, gợi nhớ giọng rao hàng chè sen ngọt lịm.', 'Hoàng hôn nhuộm tím góc trời, hàng cây khẽ đung đưa như thì thầm lời tạm biệt. Hà Nội mùa thu – khúc giao mùa dịu dàng, lưu luyến bước chân ai vội vã hay chậm rãi.']
            
            audio_service = AudioService()
            image_service = ImageService()
            
            audio_urls, image_urls = await asyncio.gather(
                audio_service.generate_audio(subtitles=subtitles, language_code=language_code, email=email),
                image_service.generate_image(subtitles=subtitles, email=email)
            )
            
            '''
            
            audio_urls = [
                'app/public/audios/nhnguyen135716@gmail.com-output0.mp3',
                'app/public/audios/nhnguyen135716@gmail.com-output1.mp3',
                'app/public/audios/nhnguyen135716@gmail.com-output2.mp3',
                'app/public/audios/nhnguyen135716@gmail.com-output3.mp3',
            ]
            
            image_urls = [
                'app/public/images/nhnguyen135716@gmail.com-output0.png',
                'app/public/images/nhnguyen135716@gmail.com-output1.png',
                'app/public/images/nhnguyen135716@gmail.com-output2.png',
                'app/public/images/nhnguyen135716@gmail.com-output3.png',
            ]'''
                        
            video_service = VideoService(
                image_urls=image_urls,
                audio_urls=audio_urls,
                subtitles=subtitles,
                topic=topic,
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
                image_path = f'app/public/images/{email}-output{i}.png'
                audio_path = f'app/public/audios/{email}-output{i}.mp3'
                
                # Append tasks to the list
                upload_image_tasks.append(cloudinary_service.upload_file(image_path, resource_type="image"))
                upload_audio_tasks.append(cloudinary_service.upload_file(audio_path, resource_type="video"))

            # Run all image and audio uploads concurrently
            image_results, audio_results = await asyncio.gather(
                asyncio.gather(*upload_image_tasks),
                asyncio.gather(*upload_audio_tasks)
            )

            # Add results to video_data
            video_data['image_urls'] = image_results
            video_data['audio_urls'] = audio_results
            video_data['subtitles'] = subtitles
            
            # Create video record in the database
            video_id = await Video.create(db, user_id=user_id, video_data=video_data)
                    
            result['id'] = video_id
            
        except Exception as e:
            print(f"Error creating video: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate video")
        
        finally:
            #delete files after video creation
            for i in range(4):
                image_path = f'app/public/images/{email}-output{i}.png'
                audio_path = f'app/public/audios/{email}-output{i}.mp3'
                if os.path.exists(image_path):
                    os.remove(image_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
        return result, 200
    
    
    @staticmethod
    async def update_video(db: AsyncSession, topic: str, email: str, video_id: int, text_effect: str=None, music: str=None, stickers: str=None):
        video = await Video.get_by_id(db, video_id)
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        try:    
            #update video
            video_service = VideoService(
                image_urls=video.image_urls,
                audio_urls=video.audio_urls,
                subtitles=video.subtitles,
                topic=topic,
                email= email
            )
            
            result = await video_service.create_video(
                text_effect=text_effect,
                music=music,
                stickers=stickers,
                need_thumbnail=False  # No need to generate thumbnail again
            )
            
            # delete old video from Cloudinary
            cloudinary_service = CloudinaryService()
            await cloudinary_service.delete_file(video.video, resource_type="video")
            
            video.video = result['video']
            
            if text_effect is not None:
                video.text_effect = text_effect
            if music is not None:
                video.music = music
            if stickers is not None:
                video.stickers = stickers
            
            await db.commit()
            await db.refresh(video)
            
            result['thumbnail'] = video.thumbnail
            
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
        
        
    @staticmethod
    async def get_videos_history(db: AsyncSession, user_id: int, number_of_videos: int):
        try:
            videos = await Video.get_videos_by_user(db, user_id, number_of_videos)
            return videos, 200
        except NoResultFound:
            raise HTTPException(status_code=404, detail="No videos found for this user")
        except Exception as e:
            print(f"Error fetching videos history: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch videos history")
        
        
    @staticmethod
    async def get_all_videos_history(db: AsyncSession, user_id: int):
        try:
            videos = await Video.get_all_videos_by_user(db, user_id)
            
            history_data = defaultdict(list)

            for video in videos:
                # Convert updated_at (datetime) to readable key, e.g., "Tue Jun 03 2025"
                date_key = video.updated_at.strftime("%a %b %d %Y")
                
                history_data[date_key].append({
                    "id": video.id,
                    "topic": video.topic,
                    "updated_at": video.updated_at.isoformat(),
                })

            return dict(history_data), 200
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    @staticmethod
    async def delete_video(db: AsyncSession, video_id: int):
        try:
            video = await Video.delete(db, video_id)
            if not video:
                raise HTTPException(status_code=404, detail="Video not found")
            
            # delete video from Cloudinary
            cloudinary_service = CloudinaryService()
            await cloudinary_service.delete_file(video.video, resource_type="video")
            
            #delete audio and image files from cloudinary
            for image_url in video.image_urls:
                await cloudinary_service.delete_file(image_url, resource_type="image")
                
            for audio_url in video.audio_urls:
                await cloudinary_service.delete_file(audio_url, resource_type="video")
                
            #delete thumbnail if exists
            if video.thumbnail:
                await cloudinary_service.delete_file(video.thumbnail, resource_type="image")
            
            return {"detail": "Video deleted successfully"}, 200
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Video not found")
        except Exception as e:
            print(f"Error deleting video: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete video")