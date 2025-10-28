import pytest

from base.api.api_client import APIClient
from dummyjson.clients.auth_client import AuthClient
from dummyjson.clients.product_client import ProductClient
from dummyjson.clients.user_client import UserClient

# Base URL for DummyJSON API
BASE_URL = "https://dummyjson.com"


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Create API client for the entire test session"""
    client = APIClient(base_url=BASE_URL, retries=2, retry_interval=0.5)
    yield client
    client.close()


@pytest.fixture(scope="function")
def product_client(api_client: APIClient) -> ProductClient:
    """Create Product client for each test"""
    return ProductClient(api_client)


@pytest.fixture(scope="function")
def user_client(api_client: APIClient) -> UserClient:
    """Create User client for each test"""
    return UserClient(api_client)


@pytest.fixture(scope="function")
def auth_client(api_client: APIClient) -> AuthClient:
    """Create Auth client for each test"""
    return AuthClient(api_client)


@pytest.fixture(scope="session")
def test_credentials() -> dict[str, str]:
    """Test user credentials for authentication tests"""
    return {"username": "emilys", "password": "emilyspass"}
