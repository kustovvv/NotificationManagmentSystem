import pytest
# from shared.tests.fixtures import client, create_test_user


class TestAuth:
    # @pytest.mark.asyncio
    # async def test_create_token(self, client, create_test_user):
    #     # Test token creation with valid credentials
    #     response = await client.post(
    #         "/auth/create_token",
    #         json={"email": "test@example.com", "password": "securepassword123"}
    #     )
    #     assert response.status_code == 201
    #     assert response.json()["success"] is True
    #     assert "access_token" in response.json()["data"]
    #
    # @pytest.mark.asyncio
    # async def test_create_token_with_incorrect_credentials(self, client, create_test_user):
    #     # Test token creation with invalid credentials
    #     response = await client.post(
    #         "/auth/create_token",
    #         json={"email": "test@example.com", "password": "wrongpassword"}
    #     )
    #     assert response.status_code == 401
    #     assert response.json()["success"] is False
    pass
