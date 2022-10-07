from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import verifyUser
from api.schemas.general import not_found_response
from database import get_db
from database.query.teachers import add_teacher_if_absent, find_teacher_by_email
from api.schemas.teachers import GetTeacherOut, PostTeacherIn, PostTeacherOut

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])


@router.get("/", 
            response_model=GetTeacherOut, 
            responses=not_found_response,
            description="Finds the teacher associated with the Google account currently logged in.")
async def __find_teacher(
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await find_teacher_by_email(db_session, teacher_email)

    if result is None:
        raise HTTPException(404, "teacher doesn't exist")

    return GetTeacherOut.from_orm(result)


@router.post("/", 
             response_model=PostTeacherOut,
             status_code=201,
             description="Creates a new teacher profile. No teacher profile should be present with the logged in account or it will fail.")
async def __create_teacher(
    teacher: PostTeacherIn,
    email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await add_teacher_if_absent(db_session, name=teacher.name, email=email)

    if result is None:
        raise HTTPException(403, "teacher already exists, try logging in!")

    return result
