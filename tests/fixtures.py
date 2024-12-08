import pytest_asyncio
from httpx import AsyncClient
from services import postgresql
from core import authentication

postgresql_client = postgresql.PostgreSQLClient()
authentication = authentication.Authentication()



@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:5000") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_user_table():
    """Cleans up the user table before and after each test."""
    postgresql_client.clean_user_table()
    yield
    postgresql_client.clean_user_table()


@pytest_asyncio.fixture(scope="function")
async def create_test_user():
    """Creates test user record in database."""
    test_email = "test@example.com"
    test_password = "securepassword123"
    test_hashed_password = authentication.get_hashed_password(test_password)
    postgresql_client.add_user(test_email, test_hashed_password)
