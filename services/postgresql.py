import os
import psycopg2
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

def db_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
                result = method(self, cursor, *args, **kwargs)
                if cursor.rowcount != -1:
                    conn.commit()
                return result
    return wrapper


class PostgreSQLClient:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")

    @db_connection
    def get_user(self, cursor, email):
        cursor.execute("SELECT * FROM public.users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user

    @db_connection
    def add_user(self, cursor, email, hashed_password):
        cursor.execute("INSERT INTO public.users (email, password) VALUES (%s, %s)", (email, hashed_password))

    @db_connection
    def clean_user_table(self, cursor):
        cursor.execute("TRUNCATE TABLE public.users RESTART IDENTITY CASCADE")

    def get_db_connection(self):
        conn = psycopg2.connect(
            host=self.DB_HOST,
            port=self.DB_PORT,
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD
        )
        return conn
