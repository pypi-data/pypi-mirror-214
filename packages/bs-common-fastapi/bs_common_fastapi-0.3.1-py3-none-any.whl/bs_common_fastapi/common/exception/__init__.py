from fastapi import status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.message = message


class NotFoundException(AppException):

    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)
