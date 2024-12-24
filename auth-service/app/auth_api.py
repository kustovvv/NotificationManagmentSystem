from fastapi import Request, HTTPException
from dotenv import load_dotenv

from .auth_service import AuthService
from shared.api.utilities_api import standard_response
from .app import app

load_dotenv()
auth_service = AuthService()

@app.post("/decode_token")
async def decode_token(request: Request):
    try:
        data = await request.json()
        user_id = await auth_service.decode_token(data.get('jwt_token'))
        return standard_response(success=True, message="Token decoded successfully", data={"user_id": user_id})
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)


@app.post("/create_token")
async def create_token(request: Request):
    try:
        data = await request.json()
        jwt_token = await auth_service.create_token(data.get('user_id'), data.get('email'))
        return standard_response(success=True, message="Token created successfully", data={"access_token": jwt_token, "token_type": "bearer"}, status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
