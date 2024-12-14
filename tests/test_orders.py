import pytest
from _pytest import mark

from tests.fixtures import client, clean_user_table, create_test_user, clean_orders_table


class TestOrders:
    @pytest.mark.asyncio
    async def test_create_order_with_missing_token(self, client, create_test_user):
        response = await client.post("/orders/create")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_order_with_invalid_token(self, client, create_test_user):
        response = await client.post("/orders/create", headers={"Authorization": "Bearer invalidtoken"})
        assert response.status_code == 401
        assert "success" not in response.json()

    @pytest.mark.asyncio
    async def test_create_order_with_invalid_order_data(self, client, create_test_user):
        # Create a token
        token_response = await client.post("/auth/create_token", json={"email": "test@example.com", "password": "securepassword123"})
        token = token_response.json()["data"]["access_token"]

        # Test order creation with valid token
        response = await client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {token}"},
            json=[{'product_id': -1, 'amount': -1}]
        )
        assert response.status_code == 500
        assert response.json()["success"] is False

    @pytest.mark.asyncio
    async def test_create_order_with_valid_order_data(self, client, create_test_user):
        # Create a token
        token_response = await client.post("/auth/create_token", json={"email": "test@example.com", "password": "securepassword123"})
        token = token_response.json()["data"]["access_token"]

        # Test order creation with valid token
        response = await client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {token}"},
            json=[{'product_id': 1, 'amount': 1}, {'product_id': 2, 'amount': 1}, {'product_id': 3, 'amount': 2}]
        )
        assert response.status_code == 201
        assert response.json()["success"] is True
        assert response.json()["message"] == "Order created successfully"
