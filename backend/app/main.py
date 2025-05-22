from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.video import video_router
from routes.trendy_fetcher import trendy_fetcher_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(video_router, prefix="/api/video", tags=["video"])
app.include_router(trendy_fetcher_router, prefix="/api/trendy_fetcher", tags=["trendy_fetcher"])
