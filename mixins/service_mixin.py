from mixins import ApplicationException
from fastapi.responses import JSONResponse
from fastapi import status
import asyncio
from typing import Union, Any


class ServiceMixin:
    def __make_response(
            self,
            code: int = status.HTTP_200_OK,
            message: str = "OK",
            body: Union[dict, list, bool] = None,
    ):
        return JSONResponse(
            status_code=code,
            content={
                "body": body if body else [] if isinstance(body, list) else {},
                "status": {"code": code, "message": message}
            }
        )

    def success_response(self, body: Union[dict, list, bool] = None):
        return self.__make_response(body=body)

    def error_response(self, code: int, message: str):
        raise ApplicationException(message=message, code=code)

    async def check_and_execute_method(self, *args) -> Any:
        result = None
        if hasattr(self, 'success_response'):
            func = getattr(self, 'success_response')
            if not func:
                raise ApplicationException(message="Такого метода не существует.", code=400)
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args)
                else:
                    result = func(*args)
            except TypeError:
                raise ApplicationException("Нет таких параметров у метода.", code=400)

        return result
