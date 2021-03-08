"""
Sets up logging to output to STDOut in Google Cloud Logging JSON format
so logs can be correlated with Google Trace
https://cloud.google.com/run/docs/logging
"""
from logging import StreamHandler, LogRecord
import json
import google.auth
from google.auth.exceptions import DefaultCredentialsError
from opentelemetry import trace
from opentelemetry.trace.span import get_hexadecimal_trace_id, get_hexadecimal_span_id


class GCloudHandler(StreamHandler):
    """
    Outputs JSON format to Stdout so Google Cloud Logging can consume
    and link logs to requests and traces
    """

    def __init__(self, project_id:str=None, stream=None):
        """
        Initialize handler

        :param project_id:      The Google Cloud Project ID to send logs to, if None
                                will look up container metadata or fall back to 'local-dev'
                                if running locally
        """
        if not project_id:
            try:
                _, self.project_id = google.auth.default()
            except DefaultCredentialsError:
                # If not set and running locally
                self.project_id = "local-dev"
        else:
            self.project_id = project_id

        super().__init__(stream)

    def format(self, record: LogRecord) -> str:

        logging_fields = {}

        current_span = trace.get_current_span()
        if current_span:
            trace_id = current_span.get_span_context().trace_id
            span_id = current_span.get_span_context().span_id
            if trace_id and span_id:
                logging_fields['logging.googleapis.com/trace'] = f"projects/{self.project_id}/traces/{get_hexadecimal_trace_id(trace_id)}"
                logging_fields['logging.googleapis.com/spanId'] = f"{get_hexadecimal_span_id(span_id)}"
                logging_fields['logging.googleapis.com/trace_sampled'] = True

        logging_fields['sourceLocation'] = {
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName
        }

        if record.exc_info:
            # Received an Exception
            e = record.exc_info[1]
            logging_fields['logging.googleapis.com/labels']['exception'] = {
                "exception": e.__class__.__name__,
                "module": e.__class__.__module__,
                "message": str(e)
            }

        # Complete a structured log entry.
        # https://cloud.google.com/logging/docs/agent/configuration#special-fields
        # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
        entry = dict(severity=record.levelname,
                     message=record.msg,
                     **logging_fields)

        return json.dumps(entry) + self.terminator
