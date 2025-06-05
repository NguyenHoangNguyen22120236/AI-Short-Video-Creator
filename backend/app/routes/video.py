from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from controllers.video import VideoController
from utils.auth import verify_jwt_token
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import get_db
from utils.schemas import VideoSchema, VideoHistorySchema

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
    x: float
    y: float
    width: float
    height: float


class VideoUpdateRequest(BaseModel):
    text_effect: Optional[str]
    music: Optional[Music]
    stickers: Optional[List[Sticker]]
    

@video_router.post("/create_video")
async def create_video(
    payload: VideoCreateRequest,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    result, status_code = await video_controller.create_video(
        db=db,
        topic=payload.topic,
        email=user_data.get("sub"),
        language_code=payload.language,
        user_id=user_data.get("user_id")
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
    
    return video # auto-converted to JSON by FastAPI


@video_router.get("/get_videos_history/{number_of_videos}", response_model=List[VideoHistorySchema])
async def get_videos_history(
    number_of_videos: int,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    videos, status_code = await video_controller.get_videos_history(
        db=db,
        user_id=user_data.get("user_id"),
        number_of_videos=number_of_videos
    )
    
    return videos # auto-converted to JSON by FastAPI


@video_router.get("/get_all_videos_history")
async def get_all_videos_history(
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    videos, status_code = await video_controller.get_all_videos_history(db=db, user_id=user_data.get("user_id"))
    if not videos:
        return JSONResponse(content={"detail": "No videos found"}, status_code=404)
    
    return JSONResponse(content=videos, status_code=status_code)


@video_router.delete("/delete_video/{video_id}")
async def delete_video(
    video_id: int,
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    result, status_code = await video_controller.delete_video(
        db=db,
        video_id=video_id,
    )
    
    if status_code == 404:
        return JSONResponse(content={"detail": "Video not found"}, status_code=404)
    
    return JSONResponse(content=result, status_code=status_code)