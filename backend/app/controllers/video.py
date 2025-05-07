import asyncio
from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService

subtitles = ['The glow of the screen illuminated Alex’s tired eyes as lines of code scrolled past. A script refused to run—until she typed “import pandas.” Errors vanished, revealing a tidy dataset.', 'Across the café table, her teammate chuckled. “Python’s like LEGO,” he said, stacking blocks of syntax. Together, they wove loops and libraries into a weather app prototype before their coffees cooled.', 'Days later, their code fueled a drone soaring over rice fields, capturing crop data. Farmers gathered, phones open, as AI mapped irrigation plans—harvests optimized by a language they’d never seen.', 'Alex smiled, rewatching the drone footage. An idea sparked: What else could we build? Somewhere, another coder stared at a blank screen, ready to type “print(“Hello, world.”)” and begin.']
audio_urls = ['public/audios/output0.mp3', 'public/audios/output1.mp3', 'public/audios/output2.mp3', 'public/audios/output3.mp3']
image_urls = ['public/images/output0.jpg', 'public/images/output1.jpg', 'public/images/output2.jpg', 'public/images/output3.jpg']

class VideoController:
    def __init__(self):
        pass
    
    async def preview_video(self, topic: str, language_code: str = "en-US"):
        if not topic:
            return {"error": "Topic is required"}, 400
        
        try:
            '''subtitles_service = SubtitlesService(topic=topic)
            subtitles = await subtitles_service.generate_subtitles()
            
            print(subtitles)

            audio_service = AudioService(subtitles=subtitles, language_code=language_code)
            image_service = ImageService()
            
            audio_urls, image_urls = await asyncio.gather(
                audio_service.generate_audio(),
                image_service.generate_image(subtitles=subtitles)
            )'''
            video_service = VideoService(subtitles=subtitles, audio_urls=audio_urls, image_urls=image_urls)
            scenes = await video_service.preview_video()
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500
        
        return {"scenes": scenes}, 200
    
    
    async def create_video(self, topic: str, language_code: str = "en-US"):
        if not topic:
            return {"error": "Topic is required"}, 400
        
        try:
           

            video_service = VideoService(subtitles=subtitles, audio_urls=audio_urls, image_urls=image_urls)
            output_path = await video_service.create_video()
        except Exception as e:
            return {"error": "Failed to generate video"}, 500
        
        return {"output_path": output_path}, 200