from rest_framework import status
from rest_framework.exceptions import APIException

from common import types_of_error


class AppError(APIException):
    """Базовое кастомное исключение для приложения."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = types_of_error.SERVER_ERROR
    default_detail = "Internal Server Error"

    def __init__(self, message=None, code=None, status_code=None, details=None):
        if status_code:
            self.status_code = status_code
        self.code = code or self.default_code
        self.details = details or None
        self.detail = message or self.default_detail

class ValidationError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = types_of_error.VALIDATION_ERROR
    default_detail = "Invalid input data"

class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = types_of_error.NOT_FOUND
    default_detail = "Resource not found"

class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = types_of_error.PERMISSION_DENIED
    default_detail = "You don't have permission to perform this action"

class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    default_code = types_of_error.CONFLICT
    default_detail = "Conflict with current resource state"