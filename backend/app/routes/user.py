from fastapi import APIRouter
from pydantic import BaseModel
from controllers.user import UserController

user_router = APIRouter()
user_controller = UserController()

class LoginRequest(BaseModel):
    email: str
    password: str

@user_router.post("/login")
def login_route(credentials: LoginRequest):
    return user_controller.login(credentials.email, credentials.password)