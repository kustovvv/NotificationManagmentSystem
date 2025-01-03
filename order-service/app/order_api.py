from fastapi import Request, HTTPException
from dotenv import load_dotenv

from shared.api.utilities_api import standard_response, decode_jwt_token
from .order_service import OrderService
from .order_db import OrdersDBClient
from .app import app

load_dotenv()
order_db_client = OrdersDBClient()


@app.post("/create")
async def create_order(request: Request):
    try:
        data = await request.json()
        jwt_token = request.headers.get('authorization')            
        user_id = await decode_jwt_token(jwt_token)
        
        order_service = OrderService(order_db_client)
        await order_service.create_order(jwt_token, user_id, data)
        return standard_response(success=True, message="Order created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
