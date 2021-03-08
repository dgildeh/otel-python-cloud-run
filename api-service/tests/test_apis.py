import logging
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)

def test_greet_api(test_client:TestClient):

    payload = { 'name': 'David', 'withError': False }
    response = test_client.post(f"/greet", json=payload)
    if response.status_code != 200:
        logger.error(f"Error Response: {response.text}")
    assert response.status_code == 200

