from fastapi.responses import JSONResponse
from mixins.service_mixin import ServiceMixin
from typing import Callable
import functools
import logging
import asyncio
import json


def normalize_data_to_log(body: dict):
    normalized_data = {}
    inner_body = body.get("body", None)
    if inner_body:
        body = inner_body
    for key, value in body.items():
        if key in ('password', 'access_token', 'refresh_token'):
            normalized_data[key] = '********************'
        else:
            normalized_data[key] = value
    return normalized_data


def log_function(logger: logging.Logger):
    def _decorator(func: Callable):
        @functools.wraps(func)
        async def _wrapper(self, *args, **kwargs):
            service_mixin = ServiceMixin()
            normalized_data = normalize_data_to_log(body=kwargs.get('body', {}))
            logger.info(
                f"{self.__class__.__name__}.{func.__name__} args: {args}; kwargs: {normalized_data};"
            )
            if asyncio.iscoroutinefunction(func):
                try:
                    result = await func(self, *args, **kwargs)
                except Exception as ex:
                    logger.error(f"{self.__class__.__name__}.{func.__name__} code: 400; returned:{ex}")
                    return service_mixin.error_response(400, str(ex))
            else:
                try:
                    result = func(*args, **kwargs)
                except Exception as ex:
                    logger.error(f"{self.__class__.__name__}.{func.__name__} code: 400; returned:{ex}")
                    return service_mixin.error_response(400, str(ex))

            status_code = result.status_code if hasattr(result, "status_code") else None

            if type(result) == JSONResponse and hasattr(result, "body"):
                normalized_data = normalize_data_to_log(body=json.loads(result.body))

            logger.info(f"{self.__class__.__name__}.{func.__name__} code: {status_code}; returned: {normalized_data};")
            return result
        return _wrapper
    return _decorator
