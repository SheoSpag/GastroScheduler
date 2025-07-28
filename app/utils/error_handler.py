from app.exceptions.customError import CustomError
from fastapi import status

def handle_exception(e: Exception, message: str = "Internal server error"):
    if isinstance(e, CustomError):
        raise e
    raise CustomError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
