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


'''from models.user import User
from utils.database import get_db
import asyncio
from utils.security import hash_password

async def create_new_user():
    async for db in get_db():
        new_user = await User.create(
            db,
            username="john cena",
            email="123@example.com",
            hashed_password=hash_password("password123"),
            auth_provider="local"
        )
        print(new_user)

if __name__ == "__main__":
    pass
    #asyncio.run(create_new_user())'''
    
    
'''from models.video import Video
from utils.database import get_db
import asyncio

video = {
    "topic": "Video 1",
    "video": "https://res.cloudinary.com/dfa9owyll/video/upload/v1748754976/engtqh8xj9vi4qctfpsu.mp4",
    "image_urls": [
            'https://res.cloudinary.com/dfa9owyll/image/upload/v1748874946/nwzsbnlmsx32cz2dbkto.jpg',
            'https://res.cloudinary.com/dfa9owyll/image/upload/v1748874947/ml8ikzms7xbsluipe89o.jpg',
            'https://res.cloudinary.com/dfa9owyll/image/upload/v1748874947/d4z5elp7gulauecjwqk2.jpg',
            'https://res.cloudinary.com/dfa9owyll/image/upload/v1748874948/qcbgqsd7hgpjdyxwvnkd.jpg'
        ],
    "audio_urls": [
            'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874949/hfnkkgcx8cta3fqd3kv5.mp3',
            'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874950/taeazcfojzmxvtx0v77u.mp3',
            'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874950/gtojem7k986oa30s72rp.mp3',
            'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874951/qqdwgejh7ba12rpmrewv.mp3'
        ],
    "subtitles": [
            f'Mat trời ló dạng qua làn sương mỏng, một bà cụ áo dài chậm rãi đẩy xe qua cánh đồng lúa xanh mướt. Tiếng cười trẻ con vang lên từ ngôi nhà mái tranh, mùi khói bếp lan tỏa.',
            f'Phố cờ đỏ sao vàng rực rỡ, tiếng rao hàng rong hòa cùng nhịp xích lô. Bàn tay thoăn thoắt gói bánh cuốn, giọt mắm cay nồng thấm vào vị giác người lữ khách.',
            f'Chiều buông xuống bến sông Hồng, mái chèo khua nước lấp lánh ánh vàng. Câu hò "ơi à ơi..." vọng từ con thuyền nan, đôi mắt người chài lưới in bóng hoàng hôn.',
            f'Đêm thành phố thức giấc trong muôn ngàn đèn hoa đăng. Bàn tay trẻ lau vội mồ hôi, gõ phím máy tính bên tách cà phê đen nóng hổi - nhịp sống mới vẫn giữ hồn xưa.'
        ],
    "text_effect": None,
    "music": {
        'title':'Funny tango dramatic music',
        'url':'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3'
    },
    "stickers": [
        {"path": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png", "x": 100, "y": 50, "width": 64, "height": 64},
        {"path": "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png", "x": 300, "y": 150, "width": 48, "height": 48}
    ]
}

async def update_video(video_id: int):
    async for db in get_db():
        
        # Save the updated object
        await Video.update(db, video_id=1, **video)
        print(f"Video with ID {video_id} updated successfully.")
        
async def get_video_by_id(video_id: int):
    async for db in get_db():
        video = await Video.get_by_id(db, video_id)
        print(video.subtitles)
        
if __name__ == "__main__":
    asyncio.run(update_video(1))'''
    
    
'''from third_party.cloudinary import CloudinaryService

email ="123@example.com"
image_urls=[
    f'public/images/{email}-output0.jpg',
    f'public/images/{email}-output1.jpg',
    f'public/images/{email}-output2.jpg',
    f'public/images/{email}-output3.jpg'
]
audio_urls=[
    f'public/audios/{email}-output0.mp3',
    f'public/audios/{email}-output1.mp3',
    f'public/audios/{email}-output2.mp3',
    f'public/audios/{email}-output3.mp3'
]

cloudinary_service = CloudinaryService()

def main():
    for image_url in image_urls:
        print(cloudinary_service.upload_image(image_url))
        
    for audio_url in audio_urls:
        print(cloudinary_service.upload_audio(audio_url))
        
if __name__ == "__main__":
    main()'''
    
'''
https://res.cloudinary.com/dfa9owyll/image/upload/v1748874946/nwzsbnlmsx32cz2dbkto.jpg
https://res.cloudinary.com/dfa9owyll/image/upload/v1748874947/ml8ikzms7xbsluipe89o.jpg
https://res.cloudinary.com/dfa9owyll/image/upload/v1748874947/d4z5elp7gulauecjwqk2.jpg
https://res.cloudinary.com/dfa9owyll/image/upload/v1748874948/qcbgqsd7hgpjdyxwvnkd.jpg
https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874949/hfnkkgcx8cta3fqd3kv5.mp3
https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874950/taeazcfojzmxvtx0v77u.mp3
https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874950/gtojem7k986oa30s72rp.mp3
https://res.cloudinary.com/dfa9owyll/raw/upload/v1748874951/qqdwgejh7ba12rpmrewv.mp3
'''