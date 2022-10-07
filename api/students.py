from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import verifyUser
from api.schemas.students import DeleteStudentOut, GetPostStudentOut, PatchStudentIn, PostStudentIn
from api.schemas.general import not_found_response
from database import get_db
from database.query.students import add_a_student, delete_a_student, find_student_by_id, update_a_student

router = APIRouter(prefix="/api/students", tags=["Students"], responses=not_found_response)


@router.get("/{student_id}",
            response_model=GetPostStudentOut,
            description="Finds a student given an id passed as a parameter.")
async def __find_a_student(
    student_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await find_student_by_id(db_session, teacher_email, student_id)

    if result is None:
        raise HTTPException(404, "student doesn't exist")

    return GetPostStudentOut.from_orm(result)


@router.post("/", 
             response_model=GetPostStudentOut, 
             status_code=201,
             description="Adds a student to a certain class of the teacher logged in.")
async def __create_a_student(
    student: PostStudentIn,
    class_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await add_a_student(db_session,
                                 teacher_email=teacher_email,
                                 class_id=class_id,
                                 name=student.name,
                                 gender=student.gender,
                                 dob=student.dob)

    if result is None:
        raise HTTPException(404, "class doesn't exist!")

    return GetPostStudentOut.from_orm(result)


@router.patch("/{student_id}", 
              response_model=GetPostStudentOut,
              description="Updates a student information given its student_id, (replaces previous info).")
async def __update_a_student(
    student_id: int,
    student: PatchStudentIn,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await update_a_student(db_session,
                                    teacher_email=teacher_email,
                                    student_id=student_id,
                                    student_in=student)

    if result is None:
        raise HTTPException(404, "student doesn't exist!")

    return GetPostStudentOut.from_orm(result)


@router.delete("/{student_id}", 
               response_model=DeleteStudentOut,
               description="Removes student from the class its in.")
async def __delete_a_student(
    student_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await delete_a_student(db_session,
                                    teacher_email=teacher_email,
                                    student_id=student_id)

    if result is None:
        raise HTTPException(404, "student doesn't exist!")

    return DeleteStudentOut()