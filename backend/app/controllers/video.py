import asyncio
from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService
from fastapi import HTTPException
import os

class VideoController:
    def __init__(self):
        pass
    
    
    async def create_video(self, topic: str, email: str, language_code: str = "en-US"):
        '''if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        try:
            subtitles_service = SubtitlesService(topic=topic, language_code=language_code)
            subtitles = await subtitles_service.generate_subtitles()
            
            audio_service = AudioService()
            image_service = ImageService()
            
            audio_urls, image_urls = await asyncio.gather(
                audio_service.generate_audio(subtitles=subtitles, language_code=language_code),
                image_service.generate_image(subtitles=subtitles)
            )
            
            video_service = VideoService(
                image_urls=image_urls,
                audio_urls=audio_urls,
                subtitles=subtitles,
                email=email
            )
            result = await video_service.create_video()
            
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
            raise HTTPException(status_code=500, detail="Failed to generate video")'''
        
        result = {
            "video": "https://res.cloudinary.com/dfa9owyll/video/upload/v1748591630/n5i6sazylxew43zmhn7o.mp4",
            "duration": 44.36,
            "subtitles": [
                {
                "text": "Mat trời ló dạng qua làn sương mỏng,",
                "start": 0,
                "end": 2.4
                },
                {
                "text": "một bà cụ áo dài chậm rãi đẩy",
                "start": 2.4,
                "end": 4.8
                },
                {
                "text": "xe qua cánh đồng lúa xanh mướt. Tiếng",
                "start": 4.8,
                "end": 7.2
                },
                {
                "text": "cười trẻ con vang lên từ ngôi nhà",
                "start": 7.2,
                "end": 9.6
                },
                {
                "text": "mái tranh, mùi khói bếp lan tỏa.",
                "start": 9.6,
                "end": 12
                },
                {
                "text": "Phố cờ đỏ sao vàng rực rỡ,",
                "start": 12,
                "end": 14.2
                },
                {
                "text": "tiếng rao hàng rong hòa cùng nhịp",
                "start": 14.2,
                "end": 16.4
                },
                {
                "text": "xích lô. Bàn tay thoăn thoắt gói",
                "start": 16.4,
                "end": 18.6
                },
                {
                "text": "bánh cuốn, giọt mắm cay nồng thấm",
                "start": 18.6,
                "end": 20.79
                },
                {
                "text": "vào vị giác người lữ khách.",
                "start": 20.79,
                "end": 22.99
                },
                {
                "text": "Chiều buông xuống bến sông Hồng, mái",
                "start": 22.99,
                "end": 25.27
                },
                {
                "text": "chèo khua nước lấp lánh ánh vàng.",
                "start": 25.27,
                "end": 27.54
                },
                {
                "text": "Câu hò \"ơi à ơi...\" vọng từ",
                "start": 27.54,
                "end": 29.82
                },
                {
                "text": "con thuyền nan, đôi mắt người",
                "start": 29.82,
                "end": 32.09
                },
                {
                "text": "chài lưới in bóng hoàng hôn.",
                "start": 32.09,
                "end": 34.37
                },
                {
                "text": "Đêm thành phố thức giấc trong muôn ngàn",
                "start": 34.37,
                "end": 36.36
                },
                {
                "text": "đèn hoa đăng. Bàn tay trẻ lau vội",
                "start": 36.36,
                "end": 38.34
                },
                {
                "text": "mồ hôi, gõ phím máy tính bên",
                "start": 38.34,
                "end": 40.33
                },
                {
                "text": "tách cà phê đen nóng hổi -",
                "start": 40.33,
                "end": 42.32
                },
                {
                "text": "nhịp sống mới vẫn giữ hồn xưa.",
                "start": 42.32,
                "end": 44.3
                }
            ]
        }
        return result, 200