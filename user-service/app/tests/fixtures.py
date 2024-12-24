import pytest_asyncio
from .. import user_db, user_service

user_db_client = user_db.UserDBClient()
user_service = user_service.UserService()


@pytest_asyncio.fixture(autouse=True)
async def clean_user_table():
    """Cleans up the user table before and after each test."""
    user_db_client.clean_user_table()
    yield
    user_db_client.clean_user_table()


@pytest_asyncio.fixture(scope="function")
async def create_test_user():
    """Creates test user record in database."""
    test_email = "test@example.com"
    test_password = "securepassword123"
    test_hashed_password = user_service.get_hashed_password(test_password)
    user_db_client.add_user(test_email, test_hashed_password)
