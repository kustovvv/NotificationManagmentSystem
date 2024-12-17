from fastapi import HTTPException
import bcrypt
from dotenv import load_dotenv

from .user_db import UserDBClient

load_dotenv()

class UserService:
    def __init__(self, db_client=None):
        self.user_db_client = db_client or UserDBClient()

    def get_user(self, email, password):
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        user = self.user_db_client.get_user(email)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized Access")

        user_id, email, hashed_password = user
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode('utf-8')

        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        return user

    def create_user(self, email, password):
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        user = self.user_db_client.get_user(email=email)
        if user:
            raise HTTPException(status_code=409, detail="Email already exists")

        hashed_password = self.get_hashed_password(password)
        self.user_db_client.add_user(email, hashed_password)

    @staticmethod
    def get_hashed_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
