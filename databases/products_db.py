from databases.utilities_db import db_connection
from databases.postgresql import PostgreSQLClient


class ProductsDBClient:
    def __init__(self):
        self.db_name = "products_service_db"
        self.postgresql_client = PostgreSQLClient(db_name=self.db_name)

    @db_connection
    def get_product(self, conn, cursor, product_id):
        cursor.execute("SELECT * FROM public.products WHERE id = %s", (product_id,))
        return cursor.fetchone()

    @db_connection
    def get_all_products(self, conn, cursor):
        cursor.execute("SELECT * FROM public.products")
        return cursor.fetchall()
