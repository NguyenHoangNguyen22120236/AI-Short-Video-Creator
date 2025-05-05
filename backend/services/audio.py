from third_party.google_cloud_api import GoogleCloudAPI

class AudioService:
    def __init__(self, subtitles, language_code):
        self.subtitles = subtitles
        self.language_code = language_code
    
    def generate_audio(self):
        google_cloud_api = GoogleCloudAPI()
        
        audio_urls = []
        
        for i, subtitle in enumerate(self.subtitles):
            print(subtitle)
            binary_data = google_cloud_api.convert_text_to_speech(str(subtitle), self.language_code)
            
            file = f'public/audios/output{i}.mp3'
            with open(file, "wb") as out:
                out.write(binary_data)  # The response's audio_content is binary.
                print("Audio content written to file f'output{i}.mp3'")
                
            audio_urls.append(file)
            
        return audio_urls

            