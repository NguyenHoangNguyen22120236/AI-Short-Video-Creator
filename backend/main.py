from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.video import video_router
from app.routes.trendy_fetcher import trendy_fetcher_router
from app.routes.user import user_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

print('FRONTEND_URL: ', os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_URL"),  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(video_router, prefix="/api/video", tags=["video"])
app.include_router(trendy_fetcher_router, prefix="/api/trendy_fetcher", tags=["trendy_fetcher"])


'''import os
import httpx
import asyncio
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("STABILITY_API_KEY")

if not api_key:
    raise Exception("Missing STABILITY_API_KEY in environment.")

# API endpoint and prompt
url = "https://api.stability.ai/v2beta/stable-image/generate/core"
prompt = "Lighthouse on a cliff overlooking the ocean"
output_path = "./lighthouse.png"

async def generate_image():
    timeout = httpx.Timeout(50.0)  # Set longer timeout
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "image/*"
                },
                files={"none": (None, '')},  # Required by Stability
                data={
                    "prompt": prompt,
                    "output_format": "png",
                    "aspect_ratio": "9:16"
                },
            )
            print("Response status code:", response.status_code)
            print('response', response)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                print("❌ Error:", e.response.json())
            except Exception:
                print("❌ Non-JSON error:", e.response.text)
            raise Exception(f"Failed to generate image. Status: {e.response.status_code}")
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved to {output_path}")

# Run async function
asyncio.run(generate_image())'''


