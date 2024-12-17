import httpx
import asyncio
from datetime import date
from fastapi import HTTPException

from .order_db import OrdersDBClient

order_db_client = OrdersDBClient()

class OrderService:
    def __init__(self):
        self.order_db_client = order_db_client
        self.default_status = 'Pending'
        self.default_price = 0
        self.product_service_url = "http://product-service:5003/products"

    async def create_order(self, user_id, order_data, creation_date=None, update_date=None):
        try:
            creation_date = creation_date or date.today()
            update_date = update_date or date.today()

            updated_order_data = self.update_order_data_with_price(order_data)
            self.order_db_client.add_order_with_items(user_id, self.default_status, self.default_price, creation_date, update_date, updated_order_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

    async def update_order_data_with_price(self, order_data):
        try:
            tasks = []
            for item in order_data:
                tasks.append(self.get_product_data(item.get('product_id')))
            product_responses = await asyncio.gather(*tasks)

            for item, product_data in zip(order_data, product_responses):
                item['price'] = product_data[4]

            return order_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order data update failed: {str(e)}")

    async def get_product_data(self, product_id):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.product_service_url}/{product_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Product data fetch failed: {str(e)}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect to Product Service: {str(e)}")


