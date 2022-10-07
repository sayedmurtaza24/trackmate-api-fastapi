from pydantic import BaseModel


class PostLoginOut(BaseModel):
    message: str = 'Login success'
    token: str | None
    