from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

from core import authentication
from services import postgresql

load_dotenv()

postgresql_client = postgresql.PostgreSQLClient()
token = authentication.Token()
authentication = authentication.Authentication()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/create_token")

def standard_response(success: bool, message: str, data=None, status_code: int = 200):
    return JSONResponse(content={"success": success, "message": message, "data": data}, status_code=status_code)

def get_current_user(jwt_token: dict=Depends(oauth2_scheme)):
    return token.decode_token(jwt_token)  # Decode the token to get user email


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


@app.post("/orders/create")
def create_order(current_user: str=Depends(get_current_user)):
    return standard_response(success=True, message="Order created successfully", data={"user": current_user})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
