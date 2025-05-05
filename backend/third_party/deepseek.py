import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

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
        try:
            data = self.__make_api_call(prompt)
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None 
        
        return data['choices'][0]['message']['content'].split('?????')
    
    
    def generate_prompt_for_image_generator(self, prompt) -> str:
        try:
            data = self.__make_api_call(prompt)
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None 
        
        return data['choices'][0]['message']['content']
    