import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
print('deepseek_api_key: ',deepseek_api_key)

class DeepSeek():
    def __init__(self):
        pass
    
    
    def __make_api_call(self, prompt):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f'Bearer {deepseek_api_key}',
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps({
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                })
            )
            
        data = response.json()
        
        return data
              
                 
    def generate_subtitles(self, prompt) -> list:  
        data:dict = self.__make_api_call(prompt)
        
        if data.get('error'):
            raise Exception(f"Error from API Deepseek: {data['error']}")
        
        raw_sections = [
            section.strip() 
            for section in str(data['choices'][0]['message']['content']).split('\n\n') 
            if section.strip()  # Removes empty/whitespace-only strings
        ]
        
        cleaned_sections = [
            section.replace("*", "").strip()  # Removes asterisks and trims whitespace
            for section in raw_sections 
            if section.strip()  # Also filters empty lines
        ]
        
        return cleaned_sections
    
    
    def generate_prompt_for_image_generator(self, prompt) -> str:
        data:dict = self.__make_api_call(prompt)
        
        if data.get('error'):
            raise Exception(f"Error from API Deepseek: {data['error']}")
        
        return data['choices'][0]['message']['content']
    