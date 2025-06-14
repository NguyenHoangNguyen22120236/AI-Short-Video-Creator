import asyncio
import requests

class RunwareAI:
    def __init__(self):
        pass

    async def generate_image(self, prompt):
        '''async def async_generate_image(prompt):
            runware = Runware(api_key=RUNWARE_API_KEY)
            await runware.connect()
            request_image = IImageInference(
                positivePrompt=prompt,
                model="civitai:101055@128078",
                numberResults=1,
                height=896,
                width=512,
            )
            images = await runware.imageInference(requestImage=request_image)
            first_image = images[0]
            
            return first_image.imageURL
                
        image_url = asyncio.run(async_generate_image(prompt=prompt))
        
        return image_url'''
        
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=360&height=640"
        response = requests.get(url)

    
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")