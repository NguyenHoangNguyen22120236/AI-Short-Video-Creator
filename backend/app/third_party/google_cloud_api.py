from google.cloud import texttospeech
from dotenv import load_dotenv
import os
import json

class GoogleCloudAPI:
    def __init__(self):
        pass

    def convert_text_to_speech(self, subtitle, language_code="en-US"):
        
        client = texttospeech.TextToSpeechClient.from_service_account_file('gcp_key.json')
        
        input_text = texttospeech.SynthesisInput(text= subtitle)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        
        return response.audio_content #Binary data of the audio file
        
            