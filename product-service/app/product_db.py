import os
from shared.databases.utilities_db import db_connection
from shared.databases.postgresql import PostgreSQLClient


class ProductsDBClient:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        self.postgresql_client = PostgreSQLClient(db_name=self.db_name, db_host=self.db_host,
                                                  db_port=self.db_port, db_user=self.db_user,
                                                  db_password=self.db_password)

    @db_connection
    def get_product(self, conn, cursor, product_id):
        cursor.execute("SELECT * FROM public.products WHERE id = %s", (product_id,))
        return cursor.fetchone()

    @db_connection
    def get_all_products(self, conn, cursor):
        cursor.execute("SELECT * FROM public.products")
        return cursor.fetchall()
