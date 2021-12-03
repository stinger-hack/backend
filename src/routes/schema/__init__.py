from pydantic import BaseModel


class BaseResponse(BaseModel):
    msg: str
    status: str
