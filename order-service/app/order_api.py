from fastapi import Request, HTTPException
from dotenv import load_dotenv

from shared.api.utilities_api import standard_response, decode_jwt_token
from shared.kafka.kafka_clients import ProductServiceClient
from .order_service import OrderService
from .order_db import OrdersDBClient
from .app import app

load_dotenv()
order_db_client = OrdersDBClient()
product_service_client = ProductServiceClient()


@app.post("/create")
async def create_order(request: Request):
    try:
        jwt_token = request.headers.get('authorization')
        if not jwt_token:
            raise HTTPException(status_code=401, detail="Token not provided")
            
        user_id = await decode_jwt_token(jwt_token)
        
        order_service = OrderService()
        data = await request.json()
        await order_service.create_order(user_id, data)
        return standard_response(success=True, message="Order created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
