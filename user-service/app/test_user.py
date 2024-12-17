import pytest
from shared.tests.fixtures import client, create_test_user


class TestUser:
    @pytest.mark.asyncio
    async def test_create_user(self, client):
        # Test successful user creation
        response = await client.post("/auth/create_user", json={"email": "test@example.com", "password": "securepassword123"})
        assert response.status_code == 201
        assert response.json()["success"] is True

    @pytest.mark.asyncio
    async def test_create_user_with_incorrect_body(self, client):
        # Test missing password in request body
        response = await client.post("/auth/create_user", json={"email": "test@example.com"})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_user_with_existing_credentials(self, client, create_test_user):
        # Test creating user with existing email
        response = await client.post("/auth/create_user", json={"email": "test@example.com", "password": "securepassword123"})
        assert response.status_code == 409
        assert response.json()["success"] is False
