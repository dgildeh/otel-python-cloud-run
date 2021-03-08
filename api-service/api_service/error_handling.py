import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class APIExceptionHandler(object):

    HTTP_CODE_MAP = {
        # The operation is not implemented or is not supported/enabled in this service.
        NotImplementedError: status.HTTP_501_NOT_IMPLEMENTED,

        # Some requested entity (e.g., file or directory) was not found.
        #  If a request is denied for some users within a class of users, such as user-based access control,
        #  PERMISSION_DENIED must be used.
        FileNotFoundError: status.HTTP_404_NOT_FOUND,

        # The entity that a client attempted to create (e.g., file or directory) already exists.
        FileExistsError: status.HTTP_409_CONFLICT,

        # The caller does not have permission to execute the specified operation.
        # PERMISSION_DENIED must not be used if the caller can not be identified (use UNAUTHENTICATED instead for those errors)
        PermissionError: status.HTTP_403_FORBIDDEN,

        # The request does not have valid authentication credentials for the operation.
        ConnectionRefusedError: status.HTTP_401_UNAUTHORIZED,

        # The client specified an invalid argument. Note that this differs from FAILED_PRECONDITION.
        ValueError: status.HTTP_400_BAD_REQUEST,

        # The operation was rejected because the system is not in a state required for the operation's execution.
        # For example, the directory to be deleted is non-empty, an rmdir operation is applied to a non-directory, etc.
        AssertionError: status.HTTP_406_NOT_ACCEPTABLE,

        # The operation was attempted past the valid range. E.g., seeking or reading past end-of-file.
        LookupError: status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,

        # The operation was aborted, typically due to a concurrency issue such as a sequencer check failure or transaction abort.
        ConnectionAbortedError: status.HTTP_424_FAILED_DEPENDENCY,

        # The operation was cancelled, typically by the caller.
        ConnectionResetError: status.HTTP_424_FAILED_DEPENDENCY,

        # Unrecoverable data loss or corruption.
        EOFError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # The deadline expired before the operation could complete.
        TimeoutError: status.HTTP_408_REQUEST_TIMEOUT,

        # Some resource has been exhausted, perhaps a per-user quota, or perhaps the entire file system is out of space.
        OverflowError: status.HTTP_403_FORBIDDEN,

        # Internal errors. This means that some invariants expected by the underlying system have been broken.
        # This error code is reserved for serious errors.
        SystemError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # The service is currently unavailable. This is most likely a transient condition,
        # which can be corrected by retrying with a backoff.
        InterruptedError: status.HTTP_503_SERVICE_UNAVAILABLE,

        # Unknown error. Catchall for any other error
        Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    @staticmethod
    def toHTTPException(error:Exception) -> HTTPException:
        """
        Convert an exception to an HTTPException with status code

        :param error:   The original Exception
        :return:        The appropriate HTTPException with correct HTTP Status Code
        """
        for errorClass, code in APIExceptionHandler.HTTP_CODE_MAP.items():
            logger.debug(f"Comparing {errorClass}=={type(error)}")
            if errorClass == type(error):
                return HTTPException(
                    status_code=code,
                    detail=str(error)
                )

        # If not found, return unknown status
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )