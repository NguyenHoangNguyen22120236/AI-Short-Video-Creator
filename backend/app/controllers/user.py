from fastapi import HTTPException
from utils.security import hash_password, verify_password
from utils.auth import create_access_token

class UserController:
    def __init__(self):
        self.fake_db = {
            "123@example.com": {
                "id": 1,
                "email": "123@example.com",
                "name": "User One",
                "hashed_password": hash_password("password123")
            }
        }

    def authenticate_user(self, email: str, password: str):
        user = self.fake_db.get(email)
        if not user or not verify_password(password, user['hashed_password']):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user

    def login(self, email: str, password: str):
        user = self.authenticate_user(email, password)
        token = create_access_token({"sub": user["email"]})
        return {"access_token": token, "token_type": "bearer"}