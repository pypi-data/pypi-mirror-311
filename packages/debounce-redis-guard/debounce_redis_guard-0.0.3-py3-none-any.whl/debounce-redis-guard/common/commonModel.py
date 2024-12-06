# MIT License
# Copyright (c) 2024 chathura deepana  ( cdeepana )
# See the LICENSE file for details.


from typing import Optional, Union
from pydantic import BaseModel


class CommonResponse(BaseModel):
    status: bool
    code: int
    data: Optional[Union[dict, list]]
    message: Optional[str]
    information: Optional[str]
    httpStatusCode: Optional[int]

    class Config:
        from_attributes = True


class RedisConfig(BaseModel):
    username: str
    password: str
    host: str
    port:str
    db: str

    class Config:
        from_attributes = True
