import logging
import grpc
from google import auth as google_auth
from google.auth.transport import grpc as google_auth_transport_grpc
from google.auth.transport import requests as google_auth_transport_requests

from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

logger = logging.getLogger(__name__)


class AuthenticatedClient(object):
    """
    Provides base utility methods to establish an authenticated
    channel on Google Cloud Run
    """

    def get_channel(self, host:str, port:int) -> grpc.Channel:
        """
        Get a secure channel initialised to make service-to-service calls
        on Google Cloud Run

        :param host:      The hostname of the service to connect to
        :param port:      The port to connect to on the service
        :returns:         A secure gRPC channel
        """

        if port == 443:
            # Setup secure channel - Google Cloud Run will provide certs and JWT authentication
            # automatically
            logger.info(f"Connecting to {host}:{port} on secure channel...")
            GrpcInstrumentorClient().instrument(channel_type='secure')

            credentials, _ = google_auth.default(scopes=(f"https://{host}",))
            request = google_auth_transport_requests.Request()
            channel = google_auth_transport_grpc.secure_authorized_channel(
                credentials, request, f"{host}:{port}")

            return channel
        else:
            logger.info(f"Connecting to {host}:{port} on insecure channel...")
            GrpcInstrumentorClient().instrument()
            channel = grpc.insecure_channel(f"{host}:{port}")
            return channel
