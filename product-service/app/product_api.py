from fastapi import Request, HTTPException
from dotenv import load_dotenv

from shared.api.utilities_api import standard_response
from .product_db import ProductsDBClient
from .app import app

load_dotenv()
product_db_client = ProductsDBClient()

@app.get("/{product_id}")
async def get_product(request: Request, product_id: int):
    try:
        product = product_db_client.get_product(product_id)
        return {"id": product[0], "category_id": product[1], "name": product[2], "is_in_stock": product[3], "price": product[4]}
    except HTTPException as e:
        return standard_response(success=False, message=e.detail, status_code=e.status_code)
