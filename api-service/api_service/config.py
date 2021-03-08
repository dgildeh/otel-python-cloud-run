import os
from pydantic import BaseSettings

class Settings(BaseSettings):

    # ----------------------------------------------------------------------------
    # HTTP listener settings
    # ----------------------------------------------------------------------------

    # Interface for the HTTP listener. Set host to 0.0.0.0 to listen on
    # all interfaces. Set to 127.0.0.1 to listen on localhost only.
    LISTEN_HOST:str = '0.0.0.0'

    # Port number for the listener.
    LISTEN_PORT:int = 5000

    # ----------------------------------------------------------------------------
    # Environment settings
    # ----------------------------------------------------------------------------

    # Environment, defaults to 'development' but can be overriden with ENVIRONMENT os variable
    ENVIRONMENT:str = os.getenv("ENVIRONMENT", "development")

    # Log Level
    LOG_LEVEL:str = os.getenv("LOG_LEVEL", "INFO")

    # Console Tracing
    TRACE_DEBUG:bool = False