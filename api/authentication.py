from fastapi import Request, HTTPException
from dotenv import load_dotenv

from app import app
from core import authentication
from api.utilities import standard_response

load_dotenv()
token = authentication.Token()
authentication = authentication.Authentication()


@app.post("/auth/create_user")
async def create_user(request: Request):
    try:
        data = await request.json()
        authentication.create_user(data.get("email"), data.get("password"))
        return standard_response(True, "User created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(False, e.detail, status_code=e.status_code)


@app.post("/auth/create_token")
async def create_token(request: Request):
    try:
        data = await request.json()
        authentication.verify_user(data.get('email'), data.get('password'))
        jwt_token = token.create_token(data.get('email'))
        return standard_response(True, "Token created successfully", data={"access_token": jwt_token, "token_type": "bearer"})
    except HTTPException as e:
        return standard_response(False, e.detail, status_code=e.status_code)
