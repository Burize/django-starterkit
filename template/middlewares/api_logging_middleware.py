import logging
from http import HTTPStatus

from rest_framework.request import Request

logger = logging.getLogger('template.api')


class APILoggingMiddleware:
    ERROR_HTTP_STATUS_CODES = [
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.SERVICE_UNAVAILABLE,
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        request.request_body = request.body

        response = self.get_response(request)

        message = f'{request.method} {request.path} {response.status_code}'
        exc_info = getattr(response, 'exc_info', None)

        if response.status_code not in self.ERROR_HTTP_STATUS_CODES:
            logger.info(message)
            return response

        message = f'{response.reason_phrase}: {message}'

        logger.error(message, exc_info=exc_info)
        return response
