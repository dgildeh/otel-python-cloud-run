import logging
from common_lib.backend_service.client import BackendServiceClient

logger = logging.getLogger(__name__)

def test_greet(backend_service_client:BackendServiceClient):

    reply = backend_service_client.greet("David", False)
    logger.info(f"Reply Received: {reply}")