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
    print(topic, language_code)
    #scenes, status_code = await video_controller.preview_video_first_time(topic, language_code)
    scenes = {'scenes': [{'image': 'https://res.cloudinary.com/dfa9owyll/image/upload/v1746690505/uejxrzzbsuk48ej3nkch.jpg', 'audio': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1746690506/uul2vw5m50bocuii6nws.mp3', 'subtitles': ['Mặt trời ló dạng qua làn sương mỏng,', 'một bà cụ áo dài chậm rãi đẩy', 'xe qua cánh đồng lúa xanh mướt. Tiếng', 'cười trẻ con vang lên từ ngôi nhà', 'mái tranh, mùi khói bếp lan tỏa.']}, {'image': 'https://res.cloudinary.com/dfa9owyll/image/upload/v1746690507/nkuz1wqqneo58cccrg2b.jpg', 'audio': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1746690508/up6hh9ncoyhdk7fvhdlr.mp3', 'subtitles': ['Phố cờ đỏ sao vàng rực rỡ,', 'tiếng rao hàng rong hòa cùng nhịp', 'xích lô. Bàn tay thoăn thoắt gói', 'bánh cuốn, giọt mắm cay nồng thấm', 'vào vị giác người lữ khách.']}, {'image': 'https://res.cloudinary.com/dfa9owyll/image/upload/v1746690509/fgqudgvmgawe2mcftgsl.jpg', 'audio': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1746690510/u04c8lfne1dilgqpongc.mp3', 'subtitles': ['Chiều buông xuống bến sông Hồng, mái', 'chèo khua nước lấp lánh ánh vàng.', 'Câu hò "ơi à ơi..." vọng từ', 'con thuyền nan, đôi mắt người', 'chài lưới in bóng hoàng hôn.']}, {'image': 'https://res.cloudinary.com/dfa9owyll/image/upload/v1746690511/ucxuifpvwovshbrvnync.jpg', 'audio': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1746690511/fjjykaajcohqzognc3tw.mp3', 'subtitles': ['Đêm thành phố thức giấc trong muôn ngàn', 'đèn hoa đăng. Bàn tay trẻ lau vội', 'mồ hôi, gõ phím máy tính bên', 'tách cà phê đen nóng hổi -', 'nhịp sống mới vẫn giữ hồn xưa.']}]}
    status_code = 200
    print(scenes)
    return JSONResponse(content=scenes, status_code=status_code)

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