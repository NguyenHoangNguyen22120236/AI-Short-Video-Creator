from services.subtitles import SubtitlesService
from services.audio import AudioService
from services.image import ImageService
from services.video import VideoService

subtitles =[
    '''In a bustling hospital, a young doctor stares at a screen filled with erratic patient data—a man’s fever won’t break, his organs failing mysteriously. She whispers, “I need help,” and taps a command. The AI system hums to life, its algorithms devouring decades of research in seconds.''',
    '''The screen flashes a rare diagnosis: an autoimmune reaction triggered by a forgotten antibiotic. The doctor’s eyes widen—she orders a targeted treatment. Across the hall, the patient’s vitals stabilize as nurses watch monitors in relieved silence.''',
    ''' Weeks later, the man walks out, hugging his daughter. A voiceover murmurs, “It’s not machines replacing us—it’s science giving us time to be human again.” The screen fades to a heartbeat line, steady and strong.'''
]

audio_urls =['public/audios/output0.mp3', 'public/audios/output1.mp3', 'public/audios/output2.mp3']
image_urls = ['public/images/output0.jpg', 'public/images/output1.jpg', 'public/images/output2.jpg']

def main():
    subtitles_service = SubtitlesService(topic="Python programming")
    subtitles = subtitles_service.generate_subtitles()
    print(subtitles)
    audio_service = AudioService(subtitles=subtitles, language_code="en-US")
    audio_urls = audio_service.generate_audio()
    print(audio_urls)
    image_service = ImageService()
    image_urls = image_service.generate_image(subtitles=subtitles)
    print(image_urls)
    video_service = VideoService(subtitles=subtitles, audio_urls=audio_urls, image_urls=image_urls)
    video_service.create_video()
    print("Video generated successfully!")

if __name__ == "__main__":
    main()