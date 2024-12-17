import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLClient:
    def __init__(self, db_name, db_host, db_port, db_user, db_password):
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password

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
