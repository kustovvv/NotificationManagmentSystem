import pytest
from tests.fixtures import client, clean_user_table, create_test_user


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_create_user(self, client):
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
    async def test_create_token(self, client, create_test_user):
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

