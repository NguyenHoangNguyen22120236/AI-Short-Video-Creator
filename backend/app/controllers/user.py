from fastapi import HTTPException
from utils.security import hash_password, verify_password
from utils.auth import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os

load_dotenv()

# email: 123@example.com
# password: password123

class UserController:
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str):
        # Query user by email asynchronously
        user = await User.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user


    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        user = await UserController.authenticate_user(db, email, password)
        token = create_access_token({
            "sub": user.email,
            "user_id": user.id
        })
        return {"access_token": token, "token_type": "bearer"}
    
    
    @staticmethod
    async def create_user(db: AsyncSession, email: str, password: str, name: str):
        hashed_password = hash_password(password)
        user_data = {
            "email": email,
            "hashed_password": hashed_password,
            "username": name,
            "auth_provider": "local" 
        }
        user = await User.create(db, **user_data)
        if not user:
            raise HTTPException(status_code=400, detail="User already exists")
        return {"user_id": user.id}
    
    
    @staticmethod
    async def google_login(db: AsyncSession, token: str):
        try:
            # Verify the token with Google
            id_info  = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
            email = id_info ['email']
            google_id = id_info ['sub']
            
            # Check if user already exists
            user = await User.get_by_email(db, email)
            if user:
                if user.google_id is None:
                    # First time logging in with Google – link account
                    user.google_id = google_id
                    await db.commit()
                if user.google_id != google_id:
                    print(f"Google ID mismatch for user {user.email}: {user.google_id} != {google_id}")
                    raise HTTPException(status_code=400, detail="Google ID mismatch")
            else:
                # User does not exist, create a new one
                user = await UserController.create_google_user(db, id_info)
                
            # Create JWT token
            token = create_access_token({
                "sub": user.email,
                "user_id": user.id
            })
            
            return {"access_token": token, "token_type": "bearer"}
    
        except ValueError as e:
            print(f"Invalid Google token: {e}")
            raise HTTPException(status_code=400, detail="Invalid Google token") from e
        
        
    @staticmethod
    async def create_google_user(db: AsyncSession, id_info: dict):
        email = id_info['email']
        google_id = id_info['sub']
        name = id_info.get('name')
        avatar = id_info.get('picture')
        
        if not email or not google_id:
            print("Missing email or Google ID in token")
            raise HTTPException(status_code=400, detail="Invalid Google token")
        
        user_data = {
            "email": email,
            "avatar": avatar,
            "google_id": google_id,
            "username": name or email.split('@')[0],  # Use name if available, else use email prefix
            "auth_provider": "google"
        }
        user = await User.create(db, **user_data)
        
        if not user:
            print(f"User with email {email} already exists")
            raise HTTPException(status_code=400, detail="User already exists")
        return user
        
        