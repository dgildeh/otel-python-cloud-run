import logging
from grpc import RpcError
from google.auth.credentials import Credentials

from common_lib.grpc import AuthenticatedClient
from common_lib.backend_service.generated.backend_service_v1_pb2_grpc import BackendServiceStub
import common_lib.backend_service.generated.service_types_v1_pb2 as service_messages
from common_lib.grpc import GrpcExceptionHandler


logger = logging.getLogger(__name__)

class BackendServiceClient(AuthenticatedClient):
    """
    gRPC Client to connect to the Backend-Service
    """

    def __init__(self, host:str, port:int, stub:BackendServiceStub = None):
        """
        Initialise the Backend Service Client

        :param host:        The hostname/URL of the Backend Service
        :param port:        The port to connect to the Backend Service
        :param stub:        (Optional) Override DataServiceStub for unit tests
        """
        self.host = host
        self.port = port

        if stub:
            self._stub = stub
        else:
            channel = self.get_channel(host, port)
            self._stub = BackendServiceStub(channel)

    ###############################################################################################
    # RPC Methods
    ###############################################################################################

    def greet(self, name:str, with_error:bool=False) -> str:
        """
        Get a user with their name

        :param name:            Name of user
        :param with_error:      (Optional) True - raise random Exception during request,
                                False (default) - no error
        :return:                "Hello {name}"
        """
        try:
            request = service_messages.GreetRequest(
                name=name,
                withError=with_error
            )
            response = self._stub.Greet(request=request)
            return response.reply
        except RpcError as rpcError:
            raise GrpcExceptionHandler.fromGrpcError(rpcError)
