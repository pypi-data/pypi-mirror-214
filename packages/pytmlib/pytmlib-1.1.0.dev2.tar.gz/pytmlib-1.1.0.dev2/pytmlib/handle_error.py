from logging import Logger
from traceback import format_exception
from typing import List
from uuid import uuid4

from flask import Response
from flask import make_response
from flask import request

from .exceptions import MethodCallException


def handle_error(logger: Logger, error: Exception) -> Response:
    error_to_handle: Exception = error.__cause__ if isinstance(error, MethodCallException) else error
    lines: List[str] = format_exception(type(error_to_handle), error_to_handle, error_to_handle.__traceback__)
    error_as_str: str = ''.join(lines)
    correlation_id: str = str(uuid4())

    logger.error(msg=f'Exception with correlation ID {correlation_id} on {request.path} [{request.method}]',
                 exc_info=error_to_handle)

    error_obj: dict = {
        'correlationId': correlation_id,
        'stackTrace': error_as_str
    }

    return make_response(error_obj, 500)
