from datetime import date
from fastapi import HTTPException

from databases.orders_db import OrdersDBClient
from databases.products_db import ProductsDBClient

order_db_client = OrdersDBClient()
product_db_client = ProductsDBClient()

class OrderService:
    def __init__(self):
        self.order_db_client = order_db_client
        self.product_db_client = product_db_client
        self.default_status = 'Pending'
        self.default_price = 0

    def create_order(self, user_id, order_data, creation_date=None, update_date=None):
        try:
            creation_date = creation_date or date.today()
            update_date = update_date or date.today()

            updated_order_data = self.update_order_data_with_price(order_data)
            self.order_db_client.add_order_with_items(user_id, self.default_status, self.default_price, creation_date, update_date, updated_order_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

    def update_order_data_with_price(self, order_data):
        try:
            for item in order_data:
                product_data = self.product_db_client.get_product(item.get('product_id'))
                item['price'] = product_data[4]
            return order_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Order data update failed: {str(e)}")
