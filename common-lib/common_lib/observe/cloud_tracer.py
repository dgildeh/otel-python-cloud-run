import logging
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from google.auth.exceptions import DefaultCredentialsError
from opentelemetry.propagators import set_global_textmap
from google.auth.credentials import Credentials
from google.cloud.trace_v2 import TraceServiceClient

from .cloud_propagator import CloudTraceFormatPropagator

logger = logging.getLogger(__name__)

def setup_tracing(console_debug:bool = False, project_id:str = None,
                  credentials:Credentials = None):
    """
    Setup Tracing on Google Cloud. The Service Account Roles must have `Cloud Trace Agent`
    Role added for traces to be ingested.

    :param console_debug:   (Optional) If running locally, do you want to see all traces in console
                            (Default False)
    :param project_id:      (Optional) Google Cloud Project instance is running in
    :param credentials:     (Optional) Pass in Google Auth Credentials if already collected
    """

    trace.set_tracer_provider(TracerProvider())
    # Using the X-Cloud-Trace-Context header
    set_global_textmap(CloudTraceFormatPropagator())

    try:
        # If running on Google Cloud and no credentials provided, will use instance
        # metadata service account credentials to initialize
        client = None
        if credentials:
            logger.info("Setting up tracing with provided credentials.")
            client = TraceServiceClient(credentials=credentials)
        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(CloudTraceSpanExporter(project_id=project_id,
                                                             client=client))
        )
        logger.info("Tracing Setup. Exporting Traces to Google Cloud.")
    except DefaultCredentialsError:
        if console_debug:
            # Not running on Google Cloud so will use console exporter
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter
            trace.get_tracer_provider().add_span_processor(
                SimpleExportSpanProcessor(ConsoleSpanExporter())
            )
            logger.info("Tracing Setup. Exporting Traces to Console.")
        else:
            logger.info("Tracing Setup with no exporter.")