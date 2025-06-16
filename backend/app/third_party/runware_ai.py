import os
from dotenv import load_dotenv
import httpx

load_dotenv()

class RunwareAI:
    def __init__(self):
        pass

    async def generate_image(self, prompt):
        
        '''url = f"https://image.pollinations.ai/prompt/{prompt}?width=360&height=640"
        response = requests.get(url)

    
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")'''
        

        api_key = os.getenv("STABILITY_API_KEY")

        if api_key is None:
            raise Exception("Missing Stability API key.")

        url = "https://api.stability.ai/v2beta/stable-image/generate/core"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "image/*"
                },
                files={"none": (None, '')},  # Required for Stability AI compatibility
                data={
                    "prompt": prompt,
                    "output_format": "png",
                    "aspect_ratio": "9:16"
                },
            )

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                try:
                    error_detail = response.json()
                except Exception:
                    error_detail = response.text
                raise Exception(f"Failed to generate image: {error_detail}") from exc

            return response.content