from flask import jsonify, request
from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService

class VideoController:
    def __init__(self):
        pass
    
    def create_video(self):
        topic = request.args.get('topic')
        language_code = request.args.get('language_code', default='en-US')
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        try:
            subtitles_service = SubtitlesService(topic=topic)
            subtitles = subtitles_service.generate_subtitles()

            audio_service = AudioService(subtitles=subtitles, language_code=language_code)
            audio_urls = audio_service.generate_audio()

            image_service = ImageService()
            image_urls = image_service.generate_image(subtitles=subtitles)

            video_service = VideoService(subtitles=subtitles, audio_urls=audio_urls, image_urls=image_urls)
            output_path = video_service.create_video()
        except Exception as e:
            return jsonify({"error": "Failed to generate video"}), 500
        
        return jsonify({"output_path": output_path}), 200