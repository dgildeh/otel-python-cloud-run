import logging
from fastapi import APIRouter

from .models import GreetRequest, GreetResponse
from api_service import backend_service
from api_service.error_handling import APIExceptionHandler

logger = logging.getLogger(__name__)

v1_router = APIRouter()


@v1_router.post("/greet", response_model=GreetResponse, operation_id="greet")
async def greet(person: GreetRequest):
    """
    Sends a simple greeting back to a user that provides their name. Will return
    `Hello {name}` in response.
    """
    try:
        logger.info(f"Calling backend-service with name={person.name}")
        reply = backend_service.greet(person.name, with_error=person.withError)
        return { 'reply': reply }
    except Exception as e:
        logger.warning(f"Error calling Greet with name={person.name}: ({type(e).__name__}) {e}")
        raise APIExceptionHandler.toHTTPException(e)



