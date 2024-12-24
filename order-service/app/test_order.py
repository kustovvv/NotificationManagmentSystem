import pytest

class TestOrders:
    @pytest.mark.asyncio
    async def test_create_order_with_invalid_order_data(self, client, auth_headers, mock_db, mock_http_client):
        response = client.post(
            "/orders/create",
            headers=auth_headers,
            json=[{'product_id': -1, 'amount': -1}]
        )
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert "Invalid order data" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_create_order_with_valid_order_data(self, client, auth_headers, mock_db, mock_http_client):
        response = client.post(
            "/orders/create",
            headers=auth_headers,
            json=[{'product_id': 1, 'amount': 1}, {'product_id': 2, 'amount': 1}, {'product_id': 3, 'amount': 2}]
        )
        assert response.status_code == 201
        assert response.json()["success"] is True
        assert response.json()["message"] == "Order created successfully"

        mock_db.add_order_with_items.assert_called_once()
