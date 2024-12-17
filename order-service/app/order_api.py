from fastapi import Request, HTTPException
from dotenv import load_dotenv

from shared.api.utilities_api import standard_response
from .order_service import OrderService
from .app import app

load_dotenv()

@app.post("/orders/create")
async def create_order(request: Request):
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return standard_response(success=False, message="Unauthorized: User ID missing", status_code=401)

        data = await request.json()
        order_service = OrderService()
        await order_service.create_order(user_id, data)
        return standard_response(success=True, message="Order created successfully", status_code=201)
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
