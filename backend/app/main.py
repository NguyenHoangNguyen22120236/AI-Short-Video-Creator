from fastapi import FastAPI
from routes.video import video_router

app = FastAPI()
app.include_router(video_router, prefix="/api/video", tags=["video"])