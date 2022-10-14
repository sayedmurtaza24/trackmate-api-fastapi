from typing import Union
from pydantic import BaseModel, Field


class PostClassIn(BaseModel):
    name: str = Field(title="Class name",
                      example="Class 3A",
                      description="Name of the teachers class to be created",
                      regex="[a-zA-Z0-9 ]+",
                      max_length=20,
                      min_length=1)
    
class PostClassOut(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class GetClassOutStudent(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
    
class GetClassOutAll(BaseModel):
    classes: Union[list[PostClassOut],None]
        
    class Config:
        orm_mode = True

class GetClassOutOne(BaseModel):
    id: int
    name: str
    students: Union[list[GetClassOutStudent],None]
    
    class Config:
        orm_mode = True
        
class WeekData(BaseModel):
    presenceRate: float
    goodPerfRate: float
    goodBehaveRate: float
        
class GetClassStatisticsOut(BaseModel):
    totalStudents: int
    presenceRateAverage: float
    goodPerfRateAverage: float
    goodBehaveRateAverage: float
    weeklyData: dict[str, WeekData] = Field(example={'23 2020': WeekData(presenceRate=100, goodPerfRate=90, goodBehaveRate=89)})
    