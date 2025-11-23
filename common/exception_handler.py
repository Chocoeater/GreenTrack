from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.exceptions import AppError



def custom_exception_handler(exc, context):
    if isinstance(exc, AppError):
        response = {
            "error": {
                "code": exc.code,
                "message": exc.detail,
                "details": exc.details
            }
        }
        return Response(response, status=exc.status_code)

    drf_response = exception_handler(exc, context)

    if drf_response is not None:
        return drf_response

    return Response({
        "error": {
            "code": "server_error",
            "message": "Unexpected server error."
        }
    })