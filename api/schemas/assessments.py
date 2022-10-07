import datetime
from pydantic import BaseModel, Field

class AssessmentIn(BaseModel):
    present: bool = Field(True,
                          title="Student presence",
                          description="Presenting presence of student on that day")
    good_perf: bool = Field(True,
                            title="Students academic performance",
                            description="Presenting a good academic performance of student on that day if true")
    good_behave: bool = Field(True,
                              title="Students behavioral performance",
                              description="Presenting a good behvioral performance of student on that day if true")
    perf_comment: str = Field(None,
                              title="Teachers comment on students academic performance",
                              example="Student performed extremely well in art class, poorly in math")
    behave_comment: str = Field(None,
                                title="Teachers comment on students behavior",
                                example="Student exhibited anger signs on multiple occassions")

class PostAssessmentIn(AssessmentIn):
    date: datetime.date = Field(title="Date of assessment",
                           example=datetime.date(2021, 1, 1))

class PatchAssessmentIn(AssessmentIn):
    pass


class GetAssessmentOut(PostAssessmentIn):
    id: int

    class Config:
        orm_mode = True
