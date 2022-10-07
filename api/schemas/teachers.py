from pydantic import BaseModel, Field

class GetTeacherClassOut(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class GetTeacherOut(BaseModel):
    id: int
    name: str
    email: str
    classes: list[GetTeacherClassOut]
    
    class Config:
        orm_mode = True


class PostTeacherOut(BaseModel):
    id: int
    name: str
    email: str
    classes: list = []
    
    class Config:
        orm_mode = True


class PostTeacherIn(BaseModel):
    name: str = Field(
        title="Teacher fullname",
        description="Teachers fullname to be added (english characters only)",
        example="John Doe",
        max_length=30,
        min_length=2,
        regex="[a-zA-Z ]+",
    )
