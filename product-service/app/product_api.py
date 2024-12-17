from fastapi import Request, HTTPException
from dotenv import load_dotenv

from shared.api.utilities_api import standard_response
from .product_db import ProductsDBClient
from .app import app

load_dotenv()
product_db_client = ProductsDBClient()

@app.get("/products/{product_id}")
async def create_order(request: Request, product_id: int):
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return standard_response(success=False, message="Unauthorized: User ID missing", status_code=401)

        product = product_db_client.get_product(product_id)
        return {"id": product[0], "category_id": product[1], "name": product[2], "is_in_stock": product[3], "price": product[4]}
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
