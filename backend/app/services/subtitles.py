from app.third_party.openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class SubtitlesService:
    def __init__(self, topic, language_code="en-US"):
        self.topic = topic
        self.language_code = language_code

    async def generate_subtitles(self):
        try:
            prompt = f'''Write a 50-second story about {self.topic} to make a YouTube short video.  
                        Just the story to tell (only the narrative passage, no titles, no labels).  
                        Divide the script naturally into 4 sections for different scenes, separated by double line breaks (\n\n).  

                        **Rules:**  
                        - Each section should have 25-35 words.
                        - Do NOT label sections (no "Part 1", "Scene 1", etc.)  
                        - Do NOT include any notes, examples, or markdown formatting (*, _)  
                        - Only provide the raw story text split by \n\n  

                        Example of desired format:  
                        [First section of story]\n\n  
                        [Second section of story]\n\n  
                        [...]\n\n  
                        [Fifth section of story]  

                        Now write about: {self.topic}. Write in {'English' if self.language_code == 'en-US' else 'Vietnamese'} language.'''
            openai = OpenAI()
            
            subtitles = await openai.generate_subtitles(prompt)
            
        except Exception as e:
            raise Exception(f"Error generating subtitles: {str(e)}")
        
        return subtitles