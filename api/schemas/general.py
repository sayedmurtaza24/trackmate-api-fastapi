from pydantic import BaseModel


class NotFoundError(BaseModel):
    message: str = "{field} doesn't exist"

class ValidationError(BaseModel):
    message: str = "Bad Request"
    
class LoginFail(BaseModel):
    message: str = "Unauthorized"

not_found_response = {404: {'model': NotFoundError}}
validation_error_response = {422: {'model': ValidationError}}
login_fail_response = {401: {'model': LoginFail}}

