import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi.testclient import TestClient
from .app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"X-Consumer-ID": "test-user-123"}

@pytest.fixture(autouse=True)
def mock_db():
    with patch('app.order_service.order_db_client') as mock:
        mock.add_order_with_items = Mock()
        yield mock

@pytest.fixture(autouse=True)
def mock_http_client():
    with patch('httpx.AsyncClient') as mock:
        client = AsyncMock()
        response = AsyncMock()
        response.status_code = 200
        response.json.return_value = [1, "Test Product", "Description", 10, 99.99]
        response.raise_for_status = Mock()
        client.get = AsyncMock(return_value=response)
        mock.return_value.__aenter__.return_value = client
        yield mock
