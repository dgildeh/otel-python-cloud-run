import logging
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

from common_lib.observe import setup_tracing, GCloudHandler

from backend_service.server import Server

if __name__ == '__main__':

    # Add logging GCloudHandler
    handlers = [GCloudHandler()]
    logging.basicConfig(level=logging.INFO, handlers=handlers)

    # Add tracing
    setup_tracing(console_debug=False)
    GrpcInstrumentorServer().instrument()

    Server.run()