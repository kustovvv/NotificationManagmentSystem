from fastapi import Depends
from dotenv import load_dotenv

from api.utilities import get_current_user, standard_response
from app import app

load_dotenv()

@app.post("/orders/create")
def create_order(current_user: str=Depends(get_current_user)):
    return standard_response(success=True, message="Order created successfully", data={"user": current_user})
