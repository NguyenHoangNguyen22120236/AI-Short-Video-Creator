from backend.models.video import VideoModel
from backend.models.audio import AudioModel
from backend.models.subtitle import SubtitleModel
from backend.models.image import ImageModel
from backend.models.optional_adjustment import OptionalAdjustmentModel
from backend.models.user import UserModel
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip

class VideoService:
    def __init__(self, image_urls, audio_urls, subtitles):
        self.image_urls = image_urls
        self.audio_urls = audio_urls
        self.subtitles = subtitles
        
    def create_video(self):
        video_clips = []
        output_path="output.mp4"
        
        for i, (image_url, audio_url) in enumerate(zip(self.image_urls, self.audio_urls)):
            audio_clip = AudioFileClip(audio_url)
            duration = audio_clip.duration
            
            img_clip = ImageClip(image_url).set_duration(duration)
            img_clip = img_clip.set_audio(audio_clip)
            
            subtitle_parts = self.__split_subtitle(self.subtitles[i], 3)  # Split subtitle into 3 parts
            
            num_parts = len(subtitle_parts)
            part_duration = duration / num_parts
            
            txt_clips = []
            for idx, part in enumerate(subtitle_parts):
                txt_clip = (TextClip(part, fontsize=60, color='white', bg_color='black')
                        .set_position(('center', 'bottom'))
                        .set_start(idx * part_duration)
                        .set_duration(part_duration))
                
                txt_clips.append(txt_clip)
                
            img_with_subtitles = CompositeVideoClip([img_clip, *txt_clips])
            
            video_clips.append(img_with_subtitles)
            
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(output_path, fps=self.fps)

        return output_path
            
            
    def __split_subtitle(subtitle, n):
        words = subtitle.split()
        k = len(words) // n  # minimum words per part
        result = []
        start = 0

        for i in range(n):
            end = start + k + (1 if i < len(words) % n else 0)
            part = ' '.join(words[start:end])
            result.append(part)
            start = end

        return result