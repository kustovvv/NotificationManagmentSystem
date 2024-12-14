from jose.exceptions import ExpiredSignatureError, JWTError
from fastapi import HTTPException
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from databases.auth_db import AuthDBClient

load_dotenv()


class AuthenticationService:
    def __init__(self, token_client=None, db_client=None):
        self.token = token_client or Token()
        self.auth_db_client = db_client or AuthDBClient()

    def verify_user(self, email, password):
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        user = self.auth_db_client.get_user(email)
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

        user = self.auth_db_client.get_user(email=email)
        if user:
            raise HTTPException(status_code=409, detail="Email already exists")

        hashed_password = self.get_hashed_password(password)
        self.auth_db_client.add_user(email, hashed_password)

    @staticmethod
    def get_hashed_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class Token:
    def __init__(self):
        self.__secret_key = os.getenv('SECRET_KEY')
        self.__encode_algorithm = os.getenv('ENCODE_ALGORITHM')
        self.__token_expire_time = 15 * 60 # 15 minutes

    def create_token(self, user_id):
        try:
            expires = datetime.utcnow() + timedelta(seconds=self.__token_expire_time)
            token = jwt.encode(claims={'user_id': user_id, 'exp': expires}, key=self.__secret_key, algorithm=self.__encode_algorithm)
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=[self.__encode_algorithm])
            return payload.get("user_id")
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
