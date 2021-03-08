from concurrent import futures
import grpc
import logging
import os
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

import common_lib.backend_service.generated.backend_service_v1_pb2_grpc as backend_service
from common_lib.observe import setup_tracing, GCloudHandler

from backend_service.service import BackendService

logger = logging.getLogger(__name__)


class Server:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        backend_service.add_BackendServiceServicer_to_server(BackendService(), server)
        port = os.getenv("PORT", "50051")
        server.add_insecure_port(f"[::]:{port}")
        logger.info(f"Starting gRPC Server on port {port}")
        server.start()
        server.wait_for_termination()

if __name__ == '__main__':

    # Add logging GCloudHandler
    handlers = [GCloudHandler()]
    logging.basicConfig(level=logging.INFO, handlers=handlers)

    # Add tracing
    setup_tracing(console_debug=False)
    GrpcInstrumentorServer().instrument()

    Server.run()