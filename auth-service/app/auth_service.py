import httpx
from fastapi import HTTPException
from .token_service import Token
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = Token()


class AuthService:
    def __init__(self, token_client=None):
        self.token = token_client or token
        self.user_service_url = 'http://user-service:5002/users'

    async def create_token(self, user_id, email):
        try:
            logger.debug(f"Attempting to create token for email: {email}")
            jwt_token = self.token.create_token(user_id)
            return jwt_token
        except Exception as e:
            logger.error(f"Token creation failed: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")

    async def decode_token(self, jwt_token):
        try:
            logger.debug(f"Attempting to decode token")
            user_id = self.token.decode_token(jwt_token)
            return user_id
        except Exception as e:
            logger.error(f"Token decode failed: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Token decode failed: {str(e)}")
