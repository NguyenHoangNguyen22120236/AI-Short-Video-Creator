from third_party.runware_ai import RunwareAI
from third_party.deepseek import DeepSeek
import asyncio

class ImageService:
    def __init__(delf):
        pass
    
    async def generate_image(self, subtitles, email):
        try:
            runware_ai = RunwareAI()
            deepseek = DeepSeek()
            image_urls = []

            async def process_subtitle(i, subtitle):
                prompt_deepseek = (
                    f"Change the following passage scene into a prompt for stability AI to understand and "
                    f"generate an image suitable for this scene (Just give the prompt, 10–15 words): {subtitle}. "
                    f"The prompt should be in English"
                )

                # Generate prompt and image sequentially per subtitle
                promt_stability_ai = await deepseek.generate_prompt_for_image_generator(prompt=prompt_deepseek)
                response = await runware_ai.generate_image(prompt=promt_stability_ai)

                if response is None:
                    return None

                file_path = f'public/images/{email}-output{i}.jpg'
                with open(file_path, "wb") as out:
                    out.write(response.content)

                return file_path

            # Create a list of coroutine tasks
            tasks = [process_subtitle(i, subtitle) for i, subtitle in enumerate(subtitles)]

            # Run all tasks concurrently
            image_urls = await asyncio.gather(*tasks)

            if any(url is None for url in image_urls):
                raise Exception("One or more images failed to generate.")

            return image_urls

        except Exception as e:
            raise Exception(f"Error generating images: {str(e)}")