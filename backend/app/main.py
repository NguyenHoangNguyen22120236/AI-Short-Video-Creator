from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.video import video_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(video_router, prefix="/api/video", tags=["video"])