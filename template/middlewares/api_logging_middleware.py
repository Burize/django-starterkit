import logging
import traceback
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
        extra = {
            'http.url': request.build_absolute_uri(request.get_full_path()),
            'http.status_code': response.status_code,
            'http.method': request.method,
            'http.request_id': request.META.get('HTTP_X_REQUEST_ID', '-'),
        }

        if request.user and request.user.id:
            if hasattr(request.user, 'account'):
                extra['account_id'] = str(request.user.account.id)

        if response.status_code not in self.ERROR_HTTP_STATUS_CODES:
            logger.info(message)
            return response

        message = f'{response.reason_phrase}: {message}'
        if exc_info:
            stack = "".join(traceback.format_exception(*exc_info))
            extra['error.message'] = response.data
            extra['error.kind'] = type(exc_info[1]).__name__
            extra['error.stack'] = stack

        logger.error(message, exc_info=exc_info)
        return response
