import os
from shared.databases.utilities_db import db_connection
from shared.databases.postgresql import PostgreSQLClient


class UserDBClient:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        self.postgresql_client = PostgreSQLClient(db_name=self.db_name, db_host=self.db_host,
                                                  db_port=self.db_port, db_user=self.db_user, db_password=self.db_password)

    @db_connection
    def get_user(self, conn, cursor, email):
        cursor.execute("SELECT * FROM public.users WHERE email = %s", (email,))
        return cursor.fetchone()

    @db_connection
    def add_user(self, conn, cursor, email, hashed_password):
        cursor.execute("INSERT INTO public.users (email, password) VALUES (%s, %s)", (email, hashed_password))

    @db_connection
    def clean_user_table(self, conn, cursor):
        cursor.execute("TRUNCATE TABLE public.users RESTART IDENTITY CASCADE")

