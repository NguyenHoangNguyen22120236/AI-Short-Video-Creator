import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
import re

load_dotenv()

cloudinary.config( 
    cloud_name = "dfa9owyll", 
    api_key = os.getenv("CLOUDFLARE_API_KEY"),
    api_secret = os.getenv("CLOUDFLARE_API_SECRET"),
    secure=True
)

class CloudinaryService:
    def __init__(self):
        pass
    
    async def upload_file(self, file_path, resource_type):
        upload_result:dict = cloudinary.uploader.upload(file_path, resource_type=resource_type)
        return upload_result.get("secure_url")
    
    
    def __extract_public_id(self, url):
        # Remove the Cloudinary domain and version
        match = re.search(r'/upload/[^/]+/(.+)\.\w+$', url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid Cloudinary URL format")
    
    
    async def delete_file(self, cloudinary_url, resource_type):
        if not cloudinary_url:
            raise ValueError("Cloudinary URL cannot be empty.")

        try:
            public_id = self.__extract_public_id(cloudinary_url)
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            
        except (ValueError, IndexError):
            raise ValueError("Could not parse public ID from Cloudinary URL.")

        return result