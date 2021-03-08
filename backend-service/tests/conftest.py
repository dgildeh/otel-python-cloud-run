import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def grpc_add_to_server():
    from common_lib.backend_service.generated.backend_service_v1_pb2_grpc import add_BackendServiceServicer_to_server
    return add_BackendServiceServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    from backend_service.server import BackendService
    logger.info("Creating BackendService()")
    return BackendService()

@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    from common_lib.backend_service.generated.backend_service_v1_pb2_grpc import BackendServiceStub
    logger.info("Creating BackendServiceStub")
    return BackendServiceStub(grpc_channel)

@pytest.fixture(scope='module')
def backend_service_client(grpc_stub):
    from common_lib.backend_service.client import BackendServiceClient
    logger.info("Creating BackendServiceClient")
    return BackendServiceClient("", 0, grpc_stub)