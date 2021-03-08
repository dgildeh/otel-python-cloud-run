import logging
import grpc
import urllib.request, urllib.error

from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

logger = logging.getLogger(__name__)


class AuthenticatedClient(object):
    """
    Provides base utility methods to establish an authenticated
    channel on Google Cloud Run
    """

    _METADATA_URL = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience={}'

    def get_token(self, audience:str) -> str:
        """
        Get a JWT Token from the Google compute metadata service
        :param audience:    The url of the service being called
        :returns:           The JWT Token
        """

        if not (audience.startswith("https://") or audience.startswith("http://")):
            raise ValueError("Audience must begin with http protocol")

        url = self._METADATA_URL.format(audience)
        headers = {'Metadata-Flavor': 'Google'}

        try:
            req = urllib.request.Request(url, None, headers)
            with urllib.request.urlopen(req) as response:
                token = response.read().decode('utf-8')
                logger.info(f"Got JWT Token from Metadata Service: {token}")
                return token
        except urllib.error.URLError as ue:
            logger.info(f"Couldn't get Identity Token from {url}")
            return ''

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
            ssl = grpc.ssl_channel_credentials()
            jwt = grpc.access_token_call_credentials(self.get_token(f"https://{host}"))
            composite_credentials = grpc.composite_channel_credentials(
                ssl, jwt
            )
            channel = grpc.secure_channel(f"{host}:{port}", composite_credentials)
            return channel
        else:
            logger.info(f"Connecting to {host}:{port} on insecure channel...")
            GrpcInstrumentorClient().instrument()
            channel = grpc.insecure_channel(f"{host}:{port}")
            return channel