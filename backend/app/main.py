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


'''from third_party.cloudinary import CloudinaryService

cloudinary_service = CloudinaryService()

for i in range(2):
    print(cloudinary_service.upload_image(f'public/stickers/{i + 1}.png'))'''
    
# bear
#https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png

#play-with-pet
#https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png
 

   
# funny-tango-dramatic-music-for-vlog-video-1-minute-150834
# https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3

# moon-dance-background-dramatic-hip-hop-music-for-video-1-minute-336929
# https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671860/im4ebjxdmebgokj47vc2.mp3

# shopping-day_medium-1-335746
# https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671862/gpixnuvp3pyntzptedbt.mp3

# youx27re-beautiful_short-1-59sec-197075
# https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671864/esxogdylyk4qhhm3lbc5.mp3
