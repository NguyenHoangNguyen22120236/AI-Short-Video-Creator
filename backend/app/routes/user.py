from fastapi import APIRouter, Depends
from pydantic import BaseModel
from controllers.user import UserController
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import get_db
from fastapi.responses import JSONResponse
from utils.auth import verify_jwt_token

user_router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str
    

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

@user_router.post("/login")
async def login_route(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await UserController.login(db=db, email=credentials.email, password=credentials.password)


@user_router.post("/signup")
async def signup_route(credentials: SignupRequest, db: AsyncSession = Depends(get_db)):
    user_data = {
        "email": credentials.email,
        "password": credentials.password,
        "name": credentials.name
    }
    user = await UserController.create_user(db=db, **user_data)
    return JSONResponse(content={"user_id": user['user_id']}, status_code=201)


@user_router.post("/google-login")
async def google_login_route(
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    return await UserController.google_login(db=db, token=data.get("id_token"))


@user_router.get("/me")
async def get_current_user(
    user_data: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    return await UserController.get_user_by_email(db=db, email=user_data.get("sub"))
    
    