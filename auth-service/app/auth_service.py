from fastapi import HTTPException
from .token_service import Token
from shared.logger.logger import logger
import time
token = Token()


class AuthService:
    def __init__(self, token_client=None):
        self.token = token_client or token

    async def create_token(self, user_id, email):
        try:
            start_time = time.time()
            logger.debug(f"Attempting to create token for email: {email}")
            jwt_token = self.token.create_token(user_id)
            end_time = time.time()
            logger.debug(f"Token creation took {end_time - start_time} seconds")
            return jwt_token
        except Exception as e:
            logger.error(f"Token creation failed: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")

    async def decode_token(self, jwt_token):
        try:
            logger.debug(f"Attempting to decode token: {jwt_token}")
            user_id = self.token.decode_token(jwt_token)
            return user_id
        except Exception as e:
            logger.error(f"Token decode failed: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Token decode failed: {str(e)}")
