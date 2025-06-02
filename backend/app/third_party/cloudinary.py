import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

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
    
    def upload_video(self, file_path):
        upload_result:dict = cloudinary.uploader.upload(file_path, resource_type="video")
        return upload_result.get("secure_url")
    
    
    def upload_audio(self, file_path):
        upload_result:dict = cloudinary.uploader.upload(file_path, resource_type="raw")
        return upload_result.get("secure_url")
    
    
    def upload_image(self, file_path):
        upload_result:dict = cloudinary.uploader.upload(file_path, resource_type="image")
        return upload_result.get("secure_url")
    
    
    def delete_file(self, cloudinary_url):
        # Extract public_id from the Cloudinary URL
        if not cloudinary_url:
            raise ValueError("Cloudinary URL cannot be empty.")
        
        parts = cloudinary_url.split('/')
        
        if len(parts) < 2:
            raise ValueError("Invalid Cloudinary URL format.")
        
        public_id = parts[-1].split('.')[0]
        
        if not public_id:
            raise ValueError("Public ID could not be extracted from the URL.")
        
        cloudinary.uploader.destroy(public_id)