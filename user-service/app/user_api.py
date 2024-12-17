from fastapi import Request, HTTPException
from dotenv import load_dotenv

from .user_service import UserService
from shared.api.utilities_api import standard_response
from .app import app

load_dotenv()
user_service = UserService()


@app.post("/users/get_user")
async def get_user(request: Request):
    try:
        data = await request.json()
        user = user_service.get_user(data.get("email"), data.get("password"))
        return standard_response(success=True, message="User retrieved successfully", data={"user_id": user[0], "email": user[1]})
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)


@app.post("/users/create_user")
async def create_user(request: Request):
    try:
        data = await request.json()
        user_service.create_user(data.get("email"), data.get("password"))
        return standard_response(success=True, message="User created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
