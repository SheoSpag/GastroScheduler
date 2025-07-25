from app.exceptions.customError import CustomError
from fastapi import status

def handle_exception(e: Exception, message: str = "Internal server error"):
    """
    If the exception is already a CustomError, it is re-raised.
    Otherwise, a new CustomError with HTTP 500 status is raised using the provided message.
    This helps maintain a clean and centralized error-handling strategy.
    """
    print(f"El error real es: {e}")
    if isinstance(e, CustomError):
        raise e
    raise CustomError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
