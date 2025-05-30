from third_party.runware_ai import RunwareAI
from third_party.deepseek import DeepSeek

class ImageService:
    def __init__(delf):
        pass
    
    async def generate_image(self, subtitles, email):
        try:
            runware_ai = RunwareAI()
            deepseek = DeepSeek()
            
            image_urls = []
            
            # Generate image for each part of the script
            for i, subtitle in enumerate(subtitles):
                prompt_deepseek = f'''Change the following passage sence into a prompt for stability AI to understand and 
                                        generate image that is suitable with this sence (Just give the prompt, from 10 - 15 words):{subtitle}.
                                        
                                        The prompt should be in English'''
                promt_atability_ai = deepseek.generate_prompt_for_image_generator(prompt=prompt_deepseek)

                response = runware_ai.generate_image(prompt=promt_atability_ai)
                
                if response is None:
                    return None
                        
                file = f'public/images/{email}-output{i}.jpg'
                with open(file, "wb") as out:
                    out.write(response.content) 
                    
                image_urls.append(file)
                
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")
            
        return image_urls