import pytest
from tests.fixtures import client, clean_user_table, create_test_user

class TestOrders:
    @pytest.mark.asyncio
    async def test_create_order(self, client, create_test_user):
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
