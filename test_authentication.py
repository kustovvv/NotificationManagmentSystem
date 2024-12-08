import pytest
import pytest_asyncio
from httpx import AsyncClient
from psycopg2.extras import RealDictCursor
from functools import wraps

from services import postgresql
from core import authentication

postgresql_client = postgresql.PostgreSQLClient()
authentication = authentication.Authentication()

@pytest_asyncio.fixture(scope="function", autouse=True)
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


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_create_user(self):
        # Test missing password in request body
        response = await client.post("/auth/create_user", json={"email": "test@example.com"})
        assert response.status_code == 400

        # Test successful user creation
        response = await client.post("/auth/create_user", json={"email": "test@example.com", "password": "securepassword123"})
        assert response.status_code == 201
        assert response.json()["success"] is True

        # Test creating user with existing email
        response = await client.post("/auth/create_user", json={"email": "test@example.com", "password": "securepassword123"})
        assert response.status_code == 409
        assert response.json()["success"] is False

    @pytest.mark.asyncio
    async def test_create_token(self, create_test_user):
        # Test token creation with valid credentials
        response = await client.post(
            "/auth/create_token",
            json={"email": "test@example.com", "password": "securepassword123"}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "access_token" in response.json()["data"]

        # Test token creation with invalid credentials
        response = await client.post(
            "/auth/create_token",
            json={"email": "test@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert response.json()["success"] is False


    @pytest.mark.asyncio
    async def test_create_order(self, create_test_user):
        # Test order creation with missing token
        response = await client.post("/orders/create")
        assert response.status_code == 401

        # Test order creation with invalid token
        response = await client.post("/orders/create", headers={"Authorization": "Bearer invalidtoken"})
        assert response.status_code == 401
        assert "success" not in response.json()

        # Create a token
        token_response = await client.post("/auth/create_token", json={"email": "test@example.com", "password": "securepassword123"})
        token = token_response.json()["data"]["access_token"]

        # Test order creation with valid token
        response = await client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["message"] == "Order created successfully"

