import logging
import traceback

from django.utils.deprecation import MiddlewareMixin

from common.exceptions import AppError

logger = logging.getLogger("errors")

class ErrorLoggingMiddleware(MiddlewareMixin):
    """Логирование всех исключений до того, как они попадут в касмтоный обработчик ошибок."""

    def process_exception(self, request, exception):
        path = request.path
        method = request.method

        if isinstance(exception, AppError):
            logger.warning(
                "AppError: %s %s | code=%s, | message=%s | details=%s",
                method,
                path,
                exception.code,
                exception.detail,
                exception.details,
            )
            return None

        logger.error(
            "Unhandled exception: %s %s \n%s",
            method,
            path,
            traceback.format_exc(),
        )

        return None