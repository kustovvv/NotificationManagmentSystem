from databases.utilities_db import db_connection
from databases.postgresql import PostgreSQLClient


class AuthDBClient:
    def __init__(self):
        self.db_name = "authentication_service_db"
        self.postgresql_client = PostgreSQLClient(db_name=self.db_name)

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

