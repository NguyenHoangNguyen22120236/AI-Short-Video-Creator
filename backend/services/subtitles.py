from third_party.deepseek import DeepSeek

class SubtitlesService:
    def __init__(self, topic):
        self.topic = topic

    def generate_subtitles(self):
        prompt = f'''Write a 50-second story about {self.topic} to make a YouTube short video. 
                    Just the story to tell (Like writing passage, only passage and no addtional information, 
                    no need title). And then divide the script into smaller parts to use for different sences. 
                    Seperate by ?????. No need to include the name scene.'''
                    
        deepseek = DeepSeek()
        
        subtitles = deepseek.generate_subtitles(prompt)
        
        return subtitles