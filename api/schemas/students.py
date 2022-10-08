import datetime
from typing import Union
from pydantic import BaseModel, Field


class GetStudentAssessmentOut(BaseModel):
    id: int
    date: str
    present: bool
    good_perf: bool
    good_behave: bool
    perf_comment: str
    behave_comment: str

    class Config:
        orm_mode = True


class GetPostStudentOut(BaseModel):
    id: int
    name: str
    dob: datetime.date
    gender: str
    emergency_contact_phone: Union[str, None]
    emergency_contact_email: Union[str, None]
    assessments: list[GetStudentAssessmentOut]

    class Config:
        orm_mode = True


class PostStudentIn(BaseModel):
    name: str = Field(title="Students name", regex="[a-zA-Z]+", example="Fredrick")
    gender: str = Field(title="Students gender (male, female or other)", regex="(male)|(female)|(other)")
    dob: datetime.date = Field(title="Students date of birth", example="1980-01-22")


class PatchStudentIn(PostStudentIn):
    emergency_contact_phone: Union[str, None] = Field(title="Students emergency contact number",
                                                regex="[0-9+]+", example="0720123123")
    emergency_contact_email: Union[str, None] = Field(title="Students emergency contact email",
                                                regex="[a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-zA-Z0-9.]+",
                                                example="someone@example.com")

class DeleteStudentOut(BaseModel):
    message: str = 'student deleted'