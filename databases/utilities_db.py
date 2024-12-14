from functools import wraps


def db_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Check if `conn` and `cursor` are explicitly provided in the arguments
        if kwargs.get('conn') and kwargs.get('cursor'):
            return method(self, *args, **kwargs)

        with self.postgresql_client.get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    return method(self, conn, cursor, *args, **kwargs)
            except Exception:
                conn.rollback()
                raise
    return wrapper
