import pytest
from fastapi.testclient import TestClient

from api_service import api

@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """
    Get an initialised TestClient
    """
    client = TestClient(api)
    yield client  # testing happens here