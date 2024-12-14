import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLClient:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password
            )
            return conn
        except psycopg2.OperationalError as e:
            raise RuntimeError(f"Unable to connect to database: {e}")
