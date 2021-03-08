# Initialize FastAPI
from fastapi import FastAPI
api = FastAPI(title="Greet APIs",
              description="Simple REST API for Testing Google Cloud Run with Google Cloud Trace.",
              version="1.0.0")

# Initialize Config Settings
from api_service.config import Settings
config:Settings = Settings()

# Logging
import logging
from common_lib.observe import GCloudHandler
logger = logging.getLogger("api")
logger.setLevel(config.LOG_LEVEL)
log_handler = GCloudHandler()
logger.addHandler(log_handler)

# Tracing
from common_lib.observe import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
setup_tracing(console_debug=config.TRACE_DEBUG)
# Instrument FastAPI app
FastAPIInstrumentor.instrument_app(api)

# Initialise Data-Service gRPC Client
from common_lib.backend_service.client import BackendServiceClient
from common_lib.grpc import ServiceDNS
host, port = ServiceDNS.get_dns('backend-service', config.ENVIRONMENT)
backend_service = BackendServiceClient(host, port)

# Add V1 API
from api_service.v1.endpoints import v1_router
api.include_router(v1_router,tags=["greetings"])