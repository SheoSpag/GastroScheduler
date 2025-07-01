from fastapi import status

class CustomError(Exception):
    def __init__(self, status_code: status, detail: str):
        self.status_code = status_code
        self.detail = detail
