from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from controllers.video import VideoController

video_router = APIRouter()
video_controller = VideoController()

@video_router.get("/create_video")
async def create_video(
    #topic: str = Query(..., description="Topic of the video"),
    #language_code: str = Query("en-US", description="Language code")
):
    pass
    #result, status_code = await video_controller.create_video(topic, language_code)
    #return JSONResponse(content=result, status_code=status_code)

@video_router.get("/preview_video_first_time")
async def preview_video(
    topic: str = Query(..., description="Topic of the video"),
    language_code: str = Query("en-US", description="Language code")
):
    scenes, status_code = await video_controller.preview_video_first_time(topic, language_code)
    print(scenes)
    return JSONResponse(content=scenes, status_code=status_code)

