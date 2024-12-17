import os
from shared.databases.utilities_db import db_connection
from shared.databases.postgresql import PostgreSQLClient


class OrdersDBClient:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        self.postgresql_client = PostgreSQLClient(db_name=self.db_name, db_host=self.db_host,
                                                  db_port=self.db_port, db_user=self.db_user, db_password=self.db_password)

    @db_connection
    def add_order_with_items(self, conn, cursor, user_id, status, total_price, creation_date, update_date, order_data):
        try:
            # Add order
            order = self.add_order(conn=conn, cursor=cursor, user_id=user_id, status=status,
                                   total_price=total_price, creation_date=creation_date, update_date=update_date)
            order_id = order[0]
            conn.commit()

            # Add items associated with the order
            total_price = 0
            for item in order_data:
                self.add_order_item(order_id, item.get('product_id'), item.get('amount'), item.get('price'))
                total_price += item.get('price') * item.get('amount')
            conn.commit()

            self.update_order_total_price(conn=conn, cursor=cursor, order_id=order_id, total_price=total_price)
            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            raise e

    @db_connection
    def add_order(self, conn, cursor, user_id, status, total_price, creation_date, update_date):
        cursor.execute("INSERT INTO public.orders (user_id, status, total_price, creation_date, update_date) "
                       "VALUES (%s, %s, %s, %s, %s)"
                       "RETURNING id;",
                       (user_id, status, total_price, creation_date, update_date))
        return cursor.fetchone()

    @db_connection
    def add_order_item(self, conn, cursor, order_id, product_id, amount, price):
        cursor.execute("INSERT INTO public.order_items (order_id, product_id, amount, price) VALUES (%s, %s, %s, %s)",
                       (order_id, product_id, amount, price))

    @db_connection
    def get_order_items(self, conn, cursor, order_id):
        cursor.execute("SELECT * FROM public.order_items WHERE order_id = %s", (order_id,))

    @db_connection
    def get_order(self, conn, cursor, user_id):
        cursor.execute("SELECT * FROM public.orders WHERE user_id = %s", (user_id,))

    @db_connection
    def update_order_total_price(self, conn, cursor, order_id, total_price):
        cursor.execute("UPDATE public.orders SET total_price = %s WHERE id = %s", (total_price, order_id))

    @db_connection
    def clean_orders_table(self, conn, cursor):
        cursor.execute("TRUNCATE public.orders RESTART IDENTITY CASCADE")

