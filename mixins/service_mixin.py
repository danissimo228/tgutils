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

    def model_to_dict(self, model: Any) -> dict:
        model_dict = model.__dict__
        del model_dict['_sa_instance_state']
        return model_dict


