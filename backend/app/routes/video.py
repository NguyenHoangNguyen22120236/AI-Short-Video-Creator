from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from controllers.video import VideoController
from utils.auth import verify_jwt_token
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import get_db
from utils.schemas import VideoSchema
from fastapi import Request

video_router = APIRouter()
video_controller = VideoController()


class VideoCreateRequest(BaseModel):
    topic: str
    language: str
    
    
class Music(BaseModel):
    id: int
    title: str
    url: str


class Sticker(BaseModel):
    id: int
    url: str
    x: int
    y: int
    width: int
    height: int


class VideoUpdateRequest(BaseModel):
    text_effect: Optional[str]
    music: Optional[Music]
    stickers: Optional[List[Sticker]]
    

@video_router.post("/create_video")
async def create_video_no_subtitles(
    payload: VideoCreateRequest,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    result, status_code = await video_controller.create_video(
        db=db,
        topic=payload.topic,
        email=user_data.get("sub"),
        language_code=payload.language
    )
    return JSONResponse(content=result, status_code=status_code)


@video_router.put("/update_video/{video_id}")
async def update_video(
    video_id: int,
    payload: VideoUpdateRequest,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    music_dict = payload.music.dict() if payload.music else None
    stickers_dict_list = [sticker.dict() for sticker in payload.stickers] if payload.stickers else []

    result, status_code = await video_controller.update_video(
        db=db,
        email=user_data.get("sub"),
        video_id=video_id,
        text_effect=payload.text_effect,
        music=music_dict,
        stickers=stickers_dict_list
    )
    
    return JSONResponse(content=result, status_code=status_code)


@video_router.get("/get_video/{video_id}", response_model=VideoSchema)
async def get_video(
    video_id: int,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
    ):
    video, status_code = await video_controller.get_video(
        db=db,
        video_id=video_id)
    if not video:
        return JSONResponse(content={"detail": "Video not found"}, status_code=404)
    
    if video.user_id != user_data.get("user_id"):
        return JSONResponse(content={"detail": "Not authorized"}, status_code=403)
    
    return video# auto-converted to JSON by FastAPI


@video_router.get("/get_videos_history")
async def get_videos_history(
    quantity: int = Query(3, description="Number of videos to retrieve"),
):
    #videos, status_code = await video_controller.get_videos_history(quantity)
    videos = {'videos': [{'video_id': 1, 'topic': 'Video 1', 'created_at': '2025-5-1', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}, 
                         {'video_id': 2, 'topic': 'Video 2', 'created_at': '2025-5-5', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}, 
                         {'video_id': 3, 'topic': 'Video 3', 'created_at': '2025-5-10', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}]}
    status_code = 200
    return JSONResponse(content=videos, status_code=status_code)