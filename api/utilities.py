from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from core import authentication


load_dotenv()
token = authentication.Token()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/create_token")


def standard_response(success: bool, message: str, data=None, status_code: int = 200):
    return JSONResponse(content={"success": success, "message": message, "data": data}, status_code=status_code)

def get_current_user(jwt_token: dict=Depends(oauth2_scheme)):
    return token.decode_token(jwt_token)  # Decode the token to get user email
