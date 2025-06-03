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
        result = await db.execute(select(User).filter_by(email=email))
        user = result.scalars().first()
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