from fastapi import HTTPException
from utils.security import hash_password, verify_password
from utils.auth import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

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
        