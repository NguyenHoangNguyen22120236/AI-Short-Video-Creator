from third_party.google_cloud_api import GoogleCloudAPI

class AudioService:
    async def generate_audio(self, subtitles, language_code, email):
        google_cloud_api = GoogleCloudAPI()
        
        audio_urls = []
        
        for i, subtitle in enumerate(subtitles):
            binary_data = google_cloud_api.convert_text_to_speech(str(subtitle), language_code)
            
            file = f'public/audios/{email}-output{i}.mp3'
            with open(file, "wb") as out:
                out.write(binary_data)  # The response's audio_content is binary.
                
            audio_urls.append(file)
            
        return audio_urls

            