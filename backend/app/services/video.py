import os
import requests
import subprocess
import json
import tempfile
import shutil
from app.third_party.cloudinary import CloudinaryService
from app.utils.draw_text import build_drawtext_filter
from app.utils.url import is_url

class VideoService:
    def __init__(self, image_urls, audio_urls, subtitles, topic ,email):
        self.image_urls = image_urls
        self.audio_urls = audio_urls
        self.subtitles = subtitles
        self.topic = topic
        self.email = email
            
            
    def __split_subtitles(self, subtitle, n):
        """Split subtitle text into parts with roughly n characters each, preserving word boundaries."""
        words = subtitle.split()
        parts = []
        current_part = ""

        for word in words:
            # Check if adding the next word would exceed the character limit
            if len(current_part) + len(word) + (1 if current_part else 0) > n:
                parts.append(current_part)
                current_part = word
            else:
                current_part += (" " if current_part else "") + word

        # Add the last part if not empty
        if current_part:
            parts.append(current_part)

        return parts
    
    
    def __get_audio_duration(self, audio_url):
        """Get duration of audio file in seconds using ffprobe."""
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_url],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return float(result.stdout.decode().strip())
    
    
    def __generate_segment_subtitles(self, parts, start_time, total_duration):
        """Generate subtitles for a segment, with timing info."""
        part_duration = total_duration / len(parts)
        segment_subs = []
        seg_start = 0
        subtitles_for_segment = []

        for idx, part in enumerate(parts):
            subs_entry = {
                "text": part,
                "start": round(start_time + seg_start, 2),
                "end": round(start_time + seg_start + part_duration, 2)
            }
            subtitles_for_segment.append(subs_entry)
            segment_subs.append(part)
            seg_start += part_duration

        return subtitles_for_segment, part_duration


    def __create_drawtext_filter(self, segment_subs, font_path, text_effect):
        """Build the ffmpeg drawtext filter string for segment subtitles."""
        return build_drawtext_filter(segment_subs, font_path=font_path, text_effect=text_effect)
    
    
    def __create_video_segment(self, image_url, audio_url, segment_subs, font_path, text_effect, temp_dir, segment_index):
        """Create a single video segment with drawtext applied."""
        duration = self.__get_audio_duration(audio_url)
        drawtext_filter = self.__create_drawtext_filter(segment_subs, font_path, text_effect)
        output_segment = os.path.join(temp_dir, f"segment_{segment_index}.mp4")

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_url,
            "-i", audio_url,
            "-vf", drawtext_filter,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            output_segment
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        return output_segment, duration
    
    
    def __concatenate_segments(self, segment_paths, temp_dir, output_path):
        """Concatenate all video segments into one final output."""
        concat_file = os.path.join(temp_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for path in segment_paths:
                f.write(f"file '{path}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            output_path
        ], check=True)
        
        
    def __mix_music_with_video(self, video_path, music_path, output_path):
        # Mix audio from video and music together, keep video stream unchanged
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", music_path,
            "-filter_complex",
            "[1:a]volume=0.5[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ]
        subprocess.run(cmd, check=True)
        
    
    def __add_stickers_to_video(self, video_path, stickers, output_path):
        # Get actual video size using subprocess + ffprobe
        def get_video_dimensions(path):
            cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "json", path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            info = json.loads(result.stdout)
            width = int(info["streams"][0]["width"])
            height = int(info["streams"][0]["height"])
            return width, height

        video_width, video_height = get_video_dimensions(video_path)

        # Prepare inputs and filter graph
        inputs = ["-i", video_path]
        filter_complex = []
        overlay_stream = "[0:v]"

        for idx, sticker in enumerate(stickers):
            inputs.extend(["-i", sticker["url"]])

            # Scale from preview size (frontend canvas) to actual video size
            scale_x = video_width / sticker["previewWidth"]
            scale_y = video_height / sticker["previewHeight"]

            real_x = int(sticker["x"] * scale_x)
            real_y = int(sticker["y"] * scale_y)
            real_w = int(sticker["width"] * scale_x)
            real_h = int(sticker["height"] * scale_y)

            scale = f"scale={real_w}:{real_h}"
            overlay_tag = f"[v{idx + 1}]"
            filter_complex.append(f"[{idx + 1}:v]{scale}{overlay_tag}")

            overlay_result = f"[tmp{idx + 1}]" if idx < len(stickers) - 1 else "[vout]"
            filter_complex.append(
                f"{overlay_stream}{overlay_tag}overlay={real_x}:{real_y}{overlay_result}"
            )
            overlay_stream = overlay_result

        # Compose and run the FFmpeg command
        cmd = [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", ";".join(filter_complex),
            "-map", "[vout]",
            "-map", "0:a?",
            "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "192k",
            output_path
        ]

        subprocess.run(cmd, check=True)
    
    
    def __download_file_from_cloudinary(self, url: str, save_dir: str, filename: str) -> str:
        '''Download a file from a Cloudinary URL and save it locally.'''
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for bad responses

        os.makedirs(save_dir, exist_ok=True)  # Create directory if needed
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return file_path
    
    
    async def __generate_and_upload_thumbnail(self, video_path, email, cloudinary_service):
        thumbnail_path = f'app/public/thumbnails/{email}-thumbnail.jpg'
        
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", "00:00:01",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            "-f", "image2",
            thumbnail_path
        ], check=True)
        
        thumbnail_url = await cloudinary_service.upload_file(thumbnail_path, resource_type="image")

        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        return thumbnail_url
        
        
    async def create_video(self, text_effect=None, music=None, stickers=None, need_thumbnail=True):
        video_segments = []
        current_time = 0
        output_path = f'app/public/videos/{self.email}-output.mp4'

        with tempfile.TemporaryDirectory() as temp_dir:
            local_stickers = None
            if stickers:
                local_stickers = []
                for i, sticker in enumerate(stickers):
                    sticker_path = self.__download_file_from_cloudinary(
                        sticker['url'], temp_dir, f'{self.email}-sticker_{i}.png'
                    )
                    # Replace URL with local path, keep other properties
                    local_stickers.append({
                        **sticker,
                        'local_path': sticker_path
                    })

            # Download music locally if provided
            local_music_path = None
            if music:
                local_music_path = self.__download_file_from_cloudinary(
                    music['url'], temp_dir, f'{self.email}-background_music.mp3'
                )
                
            for i, (image_url, audio_url, subtitle_text) in enumerate(zip(self.image_urls, self.audio_urls, self.subtitles)):
                if is_url(image_url):
                    # Download from Cloudinary
                    image_path = self.__download_file_from_cloudinary(image_url, temp_dir, f'{self.email}-image_{i}.jpg')
                else:
                    # Use local path directly
                    image_path = image_url

                if is_url(audio_url):
                    audio_path = self.__download_file_from_cloudinary(audio_url, temp_dir, f'{self.email}-audio_{i}.mp3')
                else:
                    audio_path = audio_url

                parts = self.__split_subtitles(subtitle_text, 30)

                # Generate segment subtitles with timing relative to total video
                segment_subs, part_duration = self.__generate_segment_subtitles(parts, current_time, self.__get_audio_duration(audio_url))

                # Create segment video
                segment_path, duration = self.__create_video_segment(
                    image_path, audio_path, segment_subs,
                    font_path=None, # Use default font
                    text_effect=text_effect,
                    temp_dir=temp_dir,
                    segment_index=i
                )
                video_segments.append(segment_path)
                current_time += duration

            #Concatenate segments into full video WITHOUT music
            concatenated_video_path = os.path.join(temp_dir, f'{self.email}-concatenated.mp4')
            self.__concatenate_segments(video_segments, temp_dir, concatenated_video_path)
            
            if local_music_path:
                self.__mix_music_with_video(concatenated_video_path, local_music_path, output_path)
            else:
                shutil.move(concatenated_video_path, output_path)

            if local_stickers:
                temp_sticker_path = os.path.join(temp_dir, f'{self.email}-with_stickers.mp4')
                self.__add_stickers_to_video(output_path, local_stickers, temp_sticker_path)
                shutil.move(temp_sticker_path, output_path)

        # Get final video duration
        final_duration = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", output_path
        ]).decode().strip())

        
        # Upload video to Cloudinary
        cloudinary_service = CloudinaryService()
        video_url = await cloudinary_service.upload_file(output_path, resource_type="video")

        # Thumbnail generation and upload
        if need_thumbnail:
            thumbnail_url = await self.__generate_and_upload_thumbnail(output_path, self.email, cloudinary_service)
        
        # delete output video file after upload
        if os.path.exists(output_path):
            os.remove(output_path)

        return {
            "video": video_url,
            "topic": self.topic,
            "thumbnail": thumbnail_url if need_thumbnail else None,
            "music": music,
            "text_effect": text_effect,
            "stickers": stickers,
        }