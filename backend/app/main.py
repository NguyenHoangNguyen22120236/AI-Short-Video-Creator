#from fastapi import FastAPI
#from routes.video import video_router

#app = FastAPI()
#app.include_router(video_router, prefix="/api/video", tags=["video"])

from third_party.deepseek import DeepSeek

def main():
    # Initialize the DeepSeeker API client
    deep_seek = DeepSeek()
    subs = deep_seek.generate_subtitles("Python Programming")
    
    print(subs)
    
if __name__ == "__main__":
    main()