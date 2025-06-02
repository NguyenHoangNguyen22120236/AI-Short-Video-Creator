from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from controllers.video import VideoController
from utils.auth import verify_jwt_token
from pydantic import BaseModel

video_router = APIRouter()
video_controller = VideoController()


class VideoCreateRequest(BaseModel):
    topic: str
    language: str
    
    
class VideoUpdateRequest(BaseModel):
    id: int
    text_effect: str = None
    music: dict = None
    stickers: list[dict] = None
    

@video_router.post("/create_video")
async def create_video_no_subtitles(
    payload: VideoCreateRequest,
    user_data: dict = Depends(verify_jwt_token)
):
    result, status_code = await video_controller.create_video(
        topic=payload.topic,
        email=user_data.get("sub"),
        language_code=payload.language
    )
    return JSONResponse(content=result, status_code=status_code)


@video_router.post("/update_video")
async def update_video(
    payload: VideoUpdateRequest,
    user_data: dict = Depends(verify_jwt_token)
):
    result, status_code = await video_controller.update_video(
        email=user_data.get("sub"),
        id=payload.id,
        text_effect=payload.text_effect,
        music=payload.music,
        stickers=payload.stickers
    )
    return JSONResponse(content=result, status_code=status_code)


@video_router.get("/get_videos_history")
async def get_videos_history(
    quantity: int = Query(3, description="Number of videos to retrieve")
):
    #videos, status_code = await video_controller.get_videos_history(quantity)
    videos = {'videos': [{'video_id': 1, 'topic': 'Video 1', 'created_at': '2025-5-1', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}, 
                         {'video_id': 2, 'topic': 'Video 2', 'created_at': '2025-5-5', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}, 
                         {'video_id': 3, 'topic': 'Video 3', 'created_at': '2025-5-10', 'thumbnail_url': 'https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png'}]}
    status_code = 200
    return JSONResponse(content=videos, status_code=status_code)