import asyncio
from datetime import date
from fastapi import HTTPException
from shared.logger.logger import logger


class OrderService:
    def __init__(self, product_service_client, order_db_client):
        self.product_service_client = product_service_client
        self.order_db_client = order_db_client

        self.default_status = 'Pending'
        self.default_price = 0

    async def create_order(self, user_id, order_data, creation_date=None, update_date=None):
        try:
            logger.debug(f"Creating order for user {user_id}: {order_data}")
            creation_date = creation_date or date.today()
            update_date = update_date or date.today()

            if isinstance(order_data, dict):
                order_data = [order_data]

            updated_order_data = await self.update_order_data_with_price(user_id, order_data)
            self.order_db_client.add_order_with_items(user_id, self.default_status, self.default_price, creation_date, update_date, updated_order_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

    async def update_order_data_with_price(self, user_id, order_data):
        try:
            tasks = []
            for item in order_data:
                product_id = item.get('product_id')
                if not product_id:
                    raise ValueError("Missing product_id in order item")
                tasks.append(self.get_product_data(user_id, product_id))
            product_responses = await asyncio.gather(*tasks)

            for item, product_data in zip(order_data, product_responses):
                item['price'] = product_data.get('price')

            return order_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order data update failed: {str(e)}")
        finally:
            await self.product_service_client.cleanup()

    async def get_product_data(self, user_id, product_id):
        return await self.product_service_client.get_product_data(user_id, product_id)
