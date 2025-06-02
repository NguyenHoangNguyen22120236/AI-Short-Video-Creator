from fastapi import APIRouter, Depends
from pydantic import BaseModel
from controllers.user import UserController
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import get_db

user_router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@user_router.post("/login")
async def login_route(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await UserController.login(db=db, email=credentials.email, password=credentials.password)