from third_party.cloudinary import CloudinaryService
import os
import subprocess
import tempfile
from third_party.cloudinary import CloudinaryService
import srt
import datetime


class VideoService:
    def __init__(self, image_urls, audio_urls, subtitles, email):
        self.image_urls = image_urls
        self.audio_urls = audio_urls
        self.subtitles = subtitles
        self.email = email
        
    async def preview_video(self):
        cloudinary_service = CloudinaryService()
        cloudinary_image_urls = []
        cloudinary_audio_urls = []
        subtitles = []
        data_preview = zip(self.image_urls, self.audio_urls, self.subtitles)
        
        for i, (image_url, audio_url, subtitle) in enumerate(data_preview):
            cloudinary_image_url = cloudinary_service.upload_image(image_url)
            cloudinary_audio_url = cloudinary_service.upload_video(audio_url)
            
            cloudinary_image_urls.append(cloudinary_image_url)
            cloudinary_audio_urls.append(cloudinary_audio_url)
            
            subtitle_parts = self.__split_subtitle(subtitle, 5)  # Split subtitle into 3 parts
            subtitles.append(subtitle_parts)
            
        result = [
                {
                    'image': image,
                    'audio': audio,
                    'subtitles': subtitle_parts  # still a list of subtitle parts
                }
                for image, audio, subtitle_parts in zip(cloudinary_image_urls, cloudinary_audio_urls, subtitles)
            ]
        return result
    
        
    '''async def create_video(self):
        video_clips = []
        output_path="output.mp4"
        
        for i, (image_url, audio_url) in enumerate(zip(self.image_urls, self.audio_urls)):
            audio_clip = AudioFileClip(audio_url)
            duration = audio_clip.duration
            
            img_clip = ImageClip(image_url).set_duration(duration)
            img_clip = img_clip.set_audio(audio_clip)
                        
            subtitle_parts = self.__split_subtitle(self.subtitles[i], 5)  # Split subtitle into 3 parts
            
            num_parts = len(subtitle_parts)
            part_duration = duration / num_parts
            
            txt_clips = []
            for idx, part in enumerate(subtitle_parts):
                txt_clip = (TextClip(part, fontsize=35, color='white', bg_color='black')
                        .set_position((0,0.7), relative=True)
                        .set_start(idx * part_duration)
                        .set_duration(part_duration))
                
                txt_clips.append(txt_clip)
                
            img_with_subtitles = CompositeVideoClip([img_clip, *txt_clips])
            
            video_clips.append(img_with_subtitles)
            
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(output_path, fps=24, threads=10, preset='ultrafast', bitrate='1000k')

        sticker_clip: ImageClip = ImageClip('d').set_duration(duration)
        sticker_clip = sticker_clip.set_position()
        return output_path'''
            
            
    def __split_subtitle(self, subtitle, n):
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
    
    async def create_video(self):
        video_segments = []
        subtitles = []
        current_time = 0
        output_path = f'public/videos/{self.email}-output.mp4'

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, (image_url, audio_url, subtitle_text) in enumerate(zip(self.image_urls, self.audio_urls, self.subtitles)):
                # Get duration using ffprobe
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries",
                    "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_url],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                duration = float(result.stdout.decode().strip())

                # Split subtitle into parts
                parts = self.__split_subtitle(subtitle_text, 5)
                part_duration = duration / len(parts)

                # Generate SRT subtitles for this segment
                srt_subs = []
                seg_start = 0
                for idx, part in enumerate(parts):
                    start = datetime.timedelta(seconds=seg_start)
                    end = datetime.timedelta(seconds=seg_start + part_duration)
                    srt_subs.append(srt.Subtitle(index=idx+1, start=start, end=end, content=part))
                    seg_start += part_duration

                    # For returning all subtitles
                    subtitles.append({
                        "text": part,
                        "start": round(current_time, 2),
                        "end": round(current_time + part_duration, 2)
                    })
                    current_time += part_duration

                srt_path = os.path.join(temp_dir, f"segment_{i}.srt")
                with open(srt_path, "w", encoding="utf-8") as f:
                    f.write(srt.compose(srt_subs))

                # Generate temp output path
                output_segment = os.path.join(temp_dir, f"segment_{i}.mp4")
                
                print('srt_path:', srt_path)
                print("SRT file exists:", os.path.exists(srt_path))
                with open(srt_path, 'r', encoding='utf-8') as f:
                    print("--- SRT content preview ---")
                    print(f.read())
                print(f"Running ffmpeg for segment {i} with subtitles...")
                
                # Convert Windows-style path to Unix-style for FFmpeg
                srt_unix_path = srt_path.replace('\\', '/')
                if ':' in srt_unix_path:
                    drive_letter, rest = srt_unix_path.split(':', 1)
                    srt_unix_path = f"{drive_letter}\\:{rest}"

                force_style='FontName=Arial,FontSize=15,Alignment=2,Outline=1,MarginV=40'
                # Create video from image and audio using FFmpeg, burn subtitles
                subprocess.run([
                    "ffmpeg", "-y", "-loop", "1",
                    "-i", image_url,
                    "-i", audio_url,
                    "-filter_complex", f"[0:v]scale=360:640,subtitles='{srt_unix_path}:force_style={force_style}'[v]",
                    "-map", "[v]",
                    "-map", "1:a:0",
                    "-t", str(duration),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    output_segment
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                video_segments.append(output_segment)

            # Create concat file
            concat_file = os.path.join(temp_dir, "concat.txt")
            with open(concat_file, "w") as f:
                for path in video_segments:
                    f.write(f"file '{path}'\n")
            
            # Concatenate all segments
            result = subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", concat_file,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(result.stderr.decode())

        # Get final duration
        final_duration = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", output_path
        ]).decode().strip())
        
        # Upload video to Cloudinary
        '''cloudinary_service = CloudinaryService()
        video_url = cloudinary_service.upload_video(output_path)'''

        return {
            "video": output_path,
            "duration": round(final_duration, 2),
            "subtitles": subtitles
        }