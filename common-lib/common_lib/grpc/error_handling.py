import logging
import grpc

logger = logging.getLogger(__name__)


class GrpcExceptionHandler(object):
    """
    Utility class to translate to and from gRPC
    Exceptions on server and client
    """

    # Try and map GRPC Error Status Codes to Built In Exceptions
    # https://github.com/grpc/grpc/blob/master/doc/statuscodes.md
    GRPC_CODE_MAP = {
        # The operation is not implemented or is not supported/enabled in this service.
        grpc.StatusCode.UNIMPLEMENTED: NotImplementedError,

        # Some requested entity (e.g., file or directory) was not found.
        #  If a request is denied for some users within a class of users, such as user-based access control,
        #  PERMISSION_DENIED must be used.
        grpc.StatusCode.NOT_FOUND: FileNotFoundError,

        # The entity that a client attempted to create (e.g., file or directory) already exists.
        grpc.StatusCode.ALREADY_EXISTS: FileExistsError,

        # The caller does not have permission to execute the specified operation.
        # PERMISSION_DENIED must not be used if the caller can not be identified
        # (use UNAUTHENTICATED instead for those errors)
        grpc.StatusCode.PERMISSION_DENIED: PermissionError,

        # The request does not have valid authentication credentials for the operation.
        grpc.StatusCode.UNAUTHENTICATED: ConnectionRefusedError,

        # The client specified an invalid argument. Note that this differs from FAILED_PRECONDITION.
        grpc.StatusCode.INVALID_ARGUMENT: ValueError,

        # The operation was rejected because the system is not in a state required for the operation's execution.
        # For example, the directory to be deleted is non-empty, an rmdir operation is applied to a non-directory, etc.
        grpc.StatusCode.FAILED_PRECONDITION: AssertionError,

        # The operation was attempted past the valid range. E.g., seeking or reading past end-of-file.
        grpc.StatusCode.OUT_OF_RANGE: LookupError,

        # The operation was aborted, typically due to a concurrency issue such as a
        # sequencer check failure or transaction abort.
        grpc.StatusCode.ABORTED: ConnectionAbortedError,

        # The operation was cancelled, typically by the caller.
        grpc.StatusCode.CANCELLED: ConnectionResetError,

        # Unrecoverable data loss or corruption.
        grpc.StatusCode.DATA_LOSS: EOFError,

        # The deadline expired before the operation could complete.
        grpc.StatusCode.DEADLINE_EXCEEDED: TimeoutError,

        # Some resource has been exhausted, perhaps a per-user quota, or perhaps the entire file system is out of space.
        grpc.StatusCode.RESOURCE_EXHAUSTED: OverflowError,

        # Internal errors. This means that some invariants expected by the underlying system have been broken.
        # This error code is reserved for serious errors.
        grpc.StatusCode.INTERNAL: SystemError,

        # The service is currently unavailable. This is most likely a transient condition,
        # which can be corrected by retrying with a backoff.
        grpc.StatusCode.UNAVAILABLE: InterruptedError,

        # Unknown error. Catchall for any other error
        grpc.StatusCode.UNKNOWN: Exception,
    }

    @staticmethod
    def fromGrpcError(rpcError: grpc.RpcError) -> Exception:
        """
        Covert a gRPC Exception into a standard Python Exception. Uses the
        GRPC_CODE_MAP to map gRPC status codes to Python Exceptions

        :param rpcError:    The gRPC Exception with status code and details
        :returns:           The Python Exception
        """
        if rpcError.code() in GrpcExceptionHandler.GRPC_CODE_MAP:
            return GrpcExceptionHandler.GRPC_CODE_MAP[rpcError.code()](rpcError.details())
        else:
            return Exception(rpcError.details())

    @staticmethod
    def toGrpcError(error: Exception) -> (int, str):
        """
        Convert a Python Exception to a gRPC error with status code and details
        to return via the request context Uses the GRPC_CODE_MAP to map gRPC status
        codes to Python Exceptions

        :param error:   The Python Exception
        :returns:       gRPC Status int Code, and details string
        """

        # Log error - for state errors like permissions, only do warning, for more serious issues log exception
        if type(error) in [FileNotFoundError, FileExistsError, PermissionError, ValueError, AssertionError]:
            if error.__traceback__:
                trace = error.__traceback__
                log_message = f"{type(error).__name__} at {trace.tb_frame.f_code.co_filename}:" \
                              f"{trace.tb_lineno}: {str(error)}"
            else:
                log_message = f"{type(error).__name__}: {str(error)}"
            logger.warning(log_message)
        else:
            logger.exception(f"{type(error).__name__}: {str(error)}")

        for code, errorClass in GrpcExceptionHandler.GRPC_CODE_MAP.items():
            if errorClass == type(error):
                return code, str(error)

        # If not found, return unknown status
        return grpc.StatusCode.UNKNOWN, str(error)
