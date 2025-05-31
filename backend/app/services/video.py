import os
import subprocess
import tempfile
from third_party.cloudinary import CloudinaryService
from utils.draw_text import build_drawtext_filter


class VideoService:
    def __init__(self, image_urls, audio_urls, subtitles, email):
        self.image_urls = image_urls
        self.audio_urls = audio_urls
        self.subtitles = subtitles
        self.email = email
            
            
    def __split_subtitles(self, subtitle, n):
        """Split subtitle text into n parts, distributing words evenly."""
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
        
        
    async def create_video(self):
        video_segments = []
        subtitles = []
        current_time = 0
        output_path = f'public/videos/{self.email}-output.mp4'

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, (image_url, audio_url, subtitle_text) in enumerate(zip(self.image_urls, self.audio_urls, self.subtitles)):
                parts = self.__split_subtitles(subtitle_text, 5)

                # Generate segment subtitles with timing relative to total video
                segment_subs, part_duration = self.__generate_segment_subtitles(parts, current_time, self.__get_audio_duration(audio_url))
                subtitles.extend(segment_subs)

                # Create segment video
                segment_path, duration = self.__create_video_segment(
                    image_url, audio_url, segment_subs,
                    font_path="/path/to/font.ttf",
                    text_effect="wave",
                    temp_dir=temp_dir,
                    segment_index=i
                )
                video_segments.append(segment_path)
                current_time += duration

            # Concatenate all segments into final video
            self.__concatenate_segments(video_segments, temp_dir, output_path)

        # Get final video duration
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