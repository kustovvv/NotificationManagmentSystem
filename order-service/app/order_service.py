import asyncio
from fastapi import HTTPException
from shared.logger.logger import logger
import aiohttp

class OrderService:
    def __init__(self, order_db_client):
        self.order_db_client = order_db_client

        self.default_status = 'Pending'
        self.default_price = 0

    async def create_order(self, jwt_token, user_id, order_data):
        try:
            logger.debug(f"Creating order for user {user_id}: {order_data}")

            if isinstance(order_data, dict):
                order_data = [order_data]

            for item in order_data:
                if not isinstance(item, dict):
                    raise HTTPException(status_code=400, detail="Invalid order data")
                if 'product_id' not in item or 'quantity' not in item:
                    raise HTTPException(status_code=400, detail="product_id and quantity are required")
                if not isinstance(item['product_id'], int):
                    raise HTTPException(status_code=400, detail="product_id must be an integer")
                if not isinstance(item['quantity'], int):
                    raise HTTPException(status_code=400, detail="quantity must be an integer")

            updated_order_data = await self.update_order_data_with_price(jwt_token, order_data)

            self.order_db_client.add_order_with_items(user_id, self.default_status, self.default_price, updated_order_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

    async def update_order_data_with_price(self, jwt_token, order_data):
        try:
            tasks = []
            for item in order_data:
                product_id = item.get('product_id')
                if not product_id:
                    raise ValueError("Missing product_id in order item")
                tasks.append(self.get_product_data(jwt_token, product_id))
            product_responses = await asyncio.gather(*tasks)

            for item, product_data in zip(order_data, product_responses):
                item['price'] = product_data.get('price')

            return order_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order data update failed: {str(e)}")

    async def get_product_data(self, jwt_token, product_id):
        try:
            url = f"http://product-service:5003/{product_id}"
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {jwt_token}'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    return await response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get product data: {str(e)}")
