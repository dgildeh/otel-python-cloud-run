import logging
from common_lib.backend_service.generated.backend_service_v1_pb2_grpc import BackendServiceServicer
import common_lib.backend_service.generated.service_types_v1_pb2 as service_messages
from common_lib.grpc import GrpcExceptionHandler

logger = logging.getLogger(__name__)

class BackendService(BackendServiceServicer):

    def __init__(self):
        """
        Initialise service and configuration
        """
        logger.info("Initialised Backend-Service - Ready for gRPC Calls.")

    ################################################################################
    # RPC Methods
    ################################################################################

    def Greet(self, request, context):
        try:
            name = request.name if request.name else None
            with_error = request.withError

            logger.info(f"Received Greet request with name={name} and withError={with_error}")

            reply = f"Hello {name}!!"
            return service_messages.GreetResult(
                reply=reply
            )

        except Exception as e:
            code, details = GrpcExceptionHandler.toGrpcError(e)
            context.set_code(code)
            context.set_details(details)
            return service_messages.GreetResult()

