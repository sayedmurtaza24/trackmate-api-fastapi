from typing import Union
from pydantic import BaseModel


class PostLoginOut(BaseModel):
    message: str = 'Login success'
    token: Union[str,None]
    