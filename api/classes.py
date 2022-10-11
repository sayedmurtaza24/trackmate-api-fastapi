from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import verifyUser
from api.schemas.general import not_found_response
from api.schemas.classes import GetClassOutOne, GetClassStatisticsOut, PostClassIn, PostClassOut
from database.query.classes import add_a_class, find_class_by_id, get_class_statistics
from database import get_db

router = APIRouter(prefix="/api/classes", tags=["Classes"], responses=not_found_response)


@router.get("/{class_id}",
            response_model=GetClassOutOne,
            description="Finds a class given its class id.")
async def __find_a_class(
    class_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await find_class_by_id(db_session, teacher_email, class_id)

    if result is None:
        raise HTTPException(404, "class doesn't exist")

    return GetClassOutOne.from_orm(result)


@router.get("/{class_id}/statistics",
            response_model=GetClassStatisticsOut,
            description="Reports of class statistics in general and weekly basis.")
async def __get_statistics_of_a_class(
    class_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result, total_students = await get_class_statistics(db_session, teacher_email, class_id)

    if result is None:
        raise HTTPException(404, "class doesn't exist")

    presence_rate = 0
    goodperf_rate = 0
    goodbehave_rate = 0
    weekdata = {}
    total_weeks = 0
    for row in result:
        total, presence, gdperf, gdbehave, weekNo, year = row
        if weekdata.get(f"{int(weekNo)} {year}") is None:
            weekdata[f"{int(weekNo)} {year}"] = {
                'presenceRate': 0,
                'goodPerfRate': 0,
                'goodBehaveRate': 0,
            }
        weekdata.get(f"{int(weekNo)} {year}")['presenceRate'] += presence
        weekdata.get(f"{int(weekNo)} {year}")['goodPerfRate'] += gdperf
        weekdata.get(f"{int(weekNo)} {year}")['goodBehaveRate'] += gdbehave
        presence_rate += presence / total
        goodperf_rate += gdperf / total
        goodbehave_rate += gdbehave / total
        total_weeks += 1

    return GetClassStatisticsOut(
        totalStudents=total_students,
        presenceRateWeekly=presence_rate / total_weeks * 100,
        goodPerfRateWeekly=goodperf_rate / total_weeks * 100,
        goodBehaveRateWeekly=goodbehave_rate / total_weeks * 100,
        weeklyData=weekdata
    )


@router.post("/",
             response_model=PostClassOut,
             status_code=201,
             description="Creates a new class associated to the teacher currently logged in.")
async def __create_a_class(
    class_: PostClassIn,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await add_a_class(db_session, teacher_email, class_.name)

    if result is None:
        raise HTTPException(404, "teacher doesn't exist")

    return PostClassOut.from_orm(result)
