from fastapi import Depends, Request, HTTPException
from dotenv import load_dotenv

from api.utilities_api import get_current_user, standard_response
from services.order_service import OrderService
from app import app

load_dotenv()

@app.post("/orders/create")
async def create_order(request: Request, current_user: str=Depends(get_current_user)):
    try:
        data = await request.json()
        order_service = OrderService()
        order_service.create_order(current_user, data)
        return standard_response(success=True, message="Order created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
