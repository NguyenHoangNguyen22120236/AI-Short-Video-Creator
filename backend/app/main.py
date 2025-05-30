from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.video import video_router
from routes.trendy_fetcher import trendy_fetcher_router
from routes.user import user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(video_router, prefix="/api/video", tags=["video"])
app.include_router(trendy_fetcher_router, prefix="/api/trendy_fetcher", tags=["trendy_fetcher"])


'''from services.video import VideoService

video_service = VideoService(
    image_urls=[
        'public/images/output0.jpg',
        'public/images/output1.jpg',
        'public/images/output2.jpg',
        'public/images/output3.jpg'
    ],
    audio_urls=[
        'public/audios/output0.mp3',
        'public/audios/output1.mp3',
        'public/audios/output2.mp3',
        'public/audios/output3.mp3'
    ],
    subtitles=[
        'Mat trời ló dạng qua làn sương mỏng, một bà cụ áo dài chậm rãi đẩy xe qua cánh đồng lúa xanh mướt. Tiếng cười trẻ con vang lên từ ngôi nhà mái tranh, mùi khói bếp lan tỏa.',
        'Phố cờ đỏ sao vàng rực rỡ, tiếng rao hàng rong hòa cùng nhịp xích lô. Bàn tay thoăn thoắt gói bánh cuốn, giọt mắm cay nồng thấm vào vị giác người lữ khách.',
        'Chiều buông xuống bến sông Hồng, mái chèo khua nước lấp lánh ánh vàng. Câu hò "ơi à ơi..." vọng từ con thuyền nan, đôi mắt người chài lưới in bóng hoàng hôn.',
        'Đêm thành phố thức giấc trong muôn ngàn đèn hoa đăng. Bàn tay trẻ lau vội mồ hôi, gõ phím máy tính bên tách cà phê đen nóng hổi - nhịp sống mới vẫn giữ hồn xưa.'
    ]
)

print(video_service.create_video_no_subtitles())'''
'''from third_party.cloudinary import CloudinaryService

cloudinary_service = CloudinaryService()
print(cloudinary_service.upload_video('public/videos/output.mp4'))'''

'''from third_party.cloudinary import CloudinaryService

cloudinary_service = CloudinaryService()

print(cloudinary_service.upload_audio('musics/Music happy kids.mp3'))'''
# result:
# https://res.cloudinary.com/dfa9owyll/video/upload/v1748337941/rt1u8omiiqhbsbrmerlz.mp3 -----> Background music soft corporate
# https://res.cloudinary.com/dfa9owyll/video/upload/v1748338050/oh2gnk6er7wwoin5excj.mp3 -----> Cinematic ambient music beautiful sunset mood
# https://res.cloudinary.com/dfa9owyll/video/upload/v1748338080/xlaoaxquy1zthenfoftg.mp3 -----> Faded memories lofi hip hop background music
# https://res.cloudinary.com/dfa9owyll/video/upload/v1748338164/htzggi0cx0pwnvzrrsam.mp3 -----> Music happy kids



#result:
# https://res.cloudinary.com/dfa9owyll/video/upload/v1748136943/q4xi4jazlxvlsxirvfij.mp4


'''{'video': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1748136943/q4xi4jazlxvlsxirvfij.mp4', 'duration': np.float64(44.31), 'subtitles': [{'text': 'Mat trời ló dạng qua làn sương mỏng,', 'start': 0, 'end': 2.4}, {'text': 'một bà cụ áo dài chậm rãi đẩy', 'start': 2.4, 'end': 4.8}, {'text': 'xe qua cánh đồng lúa xanh mướt. Tiếng', 'start': 4.8, 'end': 7.2}, {'text': 'cười trẻ con vang lên từ ngôi nhà', 'start': 7.2, 'end': 9.6}, {'text': 'mái tranh, mùi khói bếp lan tỏa.', 'start': 9.6, 'end': 12.0}, {'text': 'Phố cờ đỏ sao vàng rực rỡ,', 'start': 12.0, 'end': 14.2}, {'text': 'tiếng rao hàng rong hòa cùng nhịp', 'start': 14.2, 'end': 16.4}, {'text': 'xích lô. Bàn tay thoăn thoắt gói', 'start': 16.4, 'end': 18.59}, {'text': 'bánh cuốn, giọt mắm cay nồng thấm', 'start': 18.59, 'end': 20.79}, {'text': 'vào vị giác người lữ khách.', 'start': 20.79, 'end': 22.99}, {'text': 'Chiều buông xuống bến sông Hồng, mái', 'start': 22.99, 'end': 25.27}, {'text': 'chèo khua nước lấp lánh ánh vàng.', 'start': 25.27, 'end': 27.54}, {'text': 'Câu hò "ơi à ơi..." vọng từ', 'start': 27.54, 'end': 29.82}, {'text': 'con thuyền nan, đôi mắt người', 'start': 29.82, 'end': 32.09}, {'text': 'chài lưới in bóng hoàng hôn.', 'start': 32.09, 'end': 34.37}, {'text': 'Đêm thành phố thức giấc trong muôn ngàn', 'start': 34.37, 'end': 36.36}, {'text': 'đèn hoa đăng. Bàn tay trẻ lau vội', 'start': 36.36, 'end': 38.35}, {'text': 'mồ hôi, gõ phím máy tính bên', 'start': 38.35, 'end': 40.33}, {'text': 'tách cà phê đen nóng hổi -', 'start': 40.33, 'end': 42.32}, {'text': 'nhịp sống mới vẫn giữ hồn xưa.', 'start': 42.32, 'end': 44.31}]}'''

