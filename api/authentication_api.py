from fastapi import Request, HTTPException
from dotenv import load_dotenv

from app import app
from services import authentication_service
from api.utilities_api import standard_response

load_dotenv()
token = authentication_service.Token()
authentication = authentication_service.AuthenticationService()


@app.post("/auth/create_user")
async def create_user(request: Request):
    try:
        data = await request.json()
        authentication.create_user(data.get("email"), data.get("password"))
        return standard_response(success=True, message="User created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)


@app.post("/auth/create_token")
async def create_token(request: Request):
    try:
        data = await request.json()
        user = authentication.verify_user(data.get('email'), data.get('password'))
        jwt_token = token.create_token(user[0])
        return standard_response(success=True, message="Token created successfully", data={"access_token": jwt_token, "token_type": "bearer"}, status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
