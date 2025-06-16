
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

class DeepSeek():
    def __init__(self):
        pass
    
    
    async def __make_api_call(self, prompt):
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f'Bearer {deepseek_api_key}',
                    "Content-Type": "application/json",
                    "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
                    "X-Title": "<YOUR_SITE_NAME>",      # Optional
                },
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            response.raise_for_status()
            return response.json()
              
                 
    async def generate_subtitles(self, prompt) -> list:  
        data:dict = await self.__make_api_call(prompt)
        
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
    
    
    async def generate_prompt_for_image_generator(self, prompt) -> str:
        data:dict = await self.__make_api_call(prompt)
        
        if data.get('error'):
            raise Exception(f"Error from API Deepseek: {data['error']}")
        
        return data['choices'][0]['message']['content']
    