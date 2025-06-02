import asyncio
from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService
from third_party.cloudinary import CloudinaryService
from fastapi import HTTPException
import os
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.video import Video

mock_video = {
    "topic": "Video 1",
    "video": "https://res.cloudinary.com/dfa9owyll/video/upload/v1748754976/engtqh8xj9vi4qctfpsu.mp4",
    "image_urls": [
            f'public/images/123@example.com-output0.jpg',
            f'public/images/123@example.com-output1.jpg',
            f'public/images/123@example.com-output2.jpg',
            f'public/images/123@example.com-output3.jpg'
        ],
    "audio_urls": [
            f'public/audios/123@example.com-output0.mp3',
            f'public/audios/123@example.com-output1.mp3',
            f'public/audios/123@example.com-output2.mp3',
            f'public/audios/123@example.com-output3.mp3'
        ],
    "subtitles": [
            f'Mat trời ló dạng qua làn sương mỏng, một bà cụ áo dài chậm rãi đẩy xe qua cánh đồng lúa xanh mướt. Tiếng cười trẻ con vang lên từ ngôi nhà mái tranh, mùi khói bếp lan tỏa.',
            f'Phố cờ đỏ sao vàng rực rỡ, tiếng rao hàng rong hòa cùng nhịp xích lô. Bàn tay thoăn thoắt gói bánh cuốn, giọt mắm cay nồng thấm vào vị giác người lữ khách.',
            f'Chiều buông xuống bến sông Hồng, mái chèo khua nước lấp lánh ánh vàng. Câu hò "ơi à ơi..." vọng từ con thuyền nan, đôi mắt người chài lưới in bóng hoàng hôn.',
            f'Đêm thành phố thức giấc trong muôn ngàn đèn hoa đăng. Bàn tay trẻ lau vội mồ hôi, gõ phím máy tính bên tách cà phê đen nóng hổi - nhịp sống mới vẫn giữ hồn xưa.'
        ],
    "text_effect": None,
    "music": {
        'title':'Funny tango dramatic music',
        'url':'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3'
    },
    "stickers": [
        {"path": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png", "x": 100, "y": 50, "width": 64, "height": 64},
        {"path": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png", "x": 300, "y": 150, "width": 48, "height": 48}
    ]
}

class VideoController:
    @staticmethod
    async def create_video(db: AsyncSession, topic: str, email: str, language_code: str = "en-US"):
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        try:
            '''subtitles_service = SubtitlesService(topic=topic, language_code=language_code)
            subtitles = await subtitles_service.generate_subtitles()
            
            audio_service = AudioService()
            image_service = ImageService()
            
            audio_urls, image_urls = await asyncio.gather(
                audio_service.generate_audio(subtitles=subtitles, language_code=language_code),
                image_service.generate_image(subtitles=subtitles)
            )'''
            
            video_service = VideoService(
                image_urls=[
                    f'public/images/{email}-output0.jpg',
                    f'public/images/{email}-output1.jpg',
                    f'public/images/{email}-output2.jpg',
                    f'public/images/{email}-output3.jpg'
                ],
                audio_urls=[
                    f'public/audios/{email}-output0.mp3',
                    f'public/audios/{email}-output1.mp3',
                    f'public/audios/{email}-output2.mp3',
                    f'public/audios/{email}-output3.mp3'
                ],
                subtitles=[
                    f'Mat trời ló dạng qua làn sương mỏng, một bà cụ áo dài chậm rãi đẩy xe qua cánh đồng lúa xanh mướt. Tiếng cười trẻ con vang lên từ ngôi nhà mái tranh, mùi khói bếp lan tỏa.',
                    f'Phố cờ đỏ sao vàng rực rỡ, tiếng rao hàng rong hòa cùng nhịp xích lô. Bàn tay thoăn thoắt gói bánh cuốn, giọt mắm cay nồng thấm vào vị giác người lữ khách.',
                    f'Chiều buông xuống bến sông Hồng, mái chèo khua nước lấp lánh ánh vàng. Câu hò "ơi à ơi..." vọng từ con thuyền nan, đôi mắt người chài lưới in bóng hoàng hôn.',
                    f'Đêm thành phố thức giấc trong muôn ngàn đèn hoa đăng. Bàn tay trẻ lau vội mồ hôi, gõ phím máy tính bên tách cà phê đen nóng hổi - nhịp sống mới vẫn giữ hồn xưa.'
                ],
                email=email
            )
            result = await video_service.create_video(
                music={
                    'id': 1,
                    'title':'Funny tango dramatic music',
                    'url':'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3'
                },
                stickers= [
                    {"url": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png", "x": 100, "y": 50, "width": 64, "height": 64},
                    {"url": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png", "x": 300, "y": 150, "width": 48, "height": 48}
                ]
                )
            
            # Upload video to Cloudinary
            '''cloudinary_service = CloudinaryService()
            video_url = cloudinary_service.upload_video(output_path)'''
            
            #delete files after video creation
            '''for i in range(len(image_urls)):
                image_path = f'public/images/{email}-output{i}.jpg'
                audio_path = f'public/audios/{email}-output{i}.mp3'
                if os.path.exists(image_path):
                    os.remove(image_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)'''
            
        except Exception as e:
            print(f"Error creating video: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate video")
        
        return result, 200
    
    
    @staticmethod
    async def update_video(db: AsyncSession, email: str, id: int, text_effect: str=None, music: str=None, stickers: str=None):
        video = await Video.get_by_id(db, id)
        
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