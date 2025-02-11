from jose.exceptions import ExpiredSignatureError, JWTError
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class Token:
    def __init__(self):
        self.__secret_key = os.getenv('JWT_SECRET')
        self.__encode_algorithm = os.getenv('JWT_ALGORITHM')
        self.__key = os.getenv('JWT_KEY')
        self.__iss = os.getenv('JWT_ISS')
        self.__token_expire_time = 15 * 60 # 15 minutes

    def create_token(self, user_id):
        try:
            headers = {}
            payload = {"kid": self.__key, 'user_id': user_id, 'exp': datetime.utcnow() + timedelta(seconds=self.__token_expire_time), "iss": self.__iss}
            token = jwt.encode(headers=headers, claims=payload, key=self.__secret_key, algorithm=self.__encode_algorithm)
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
