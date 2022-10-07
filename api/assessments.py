from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import verifyUser
from api.schemas.assessments import GetAssessmentOut, PatchAssessmentIn, PostAssessmentIn
from api.schemas.general import not_found_response
from database import get_db
from database.query.assessments import add_an_assessment, delete_an_assessment, update_an_assessment

router = APIRouter(prefix="/api/assessments", tags=["Assessments"], responses=not_found_response)


@router.post("/", 
             response_model=GetAssessmentOut, 
             status_code=201,
             description="Adds a new assessment for the student_id passed in. Date of the assessment should be unique, or else it fails.")
async def __create_an_assessment(
    assessment: PostAssessmentIn,
    student_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await add_an_assessment(db_session,
                                     teacher_email=teacher_email,
                                     student_id=student_id,
                                     assessment=assessment)

    if result is None:
        raise HTTPException(404, "student doesn't exist!")
    if result is False:
        raise HTTPException(403, "date already exists!")

    return GetAssessmentOut.from_orm(result)


@router.patch("/{assessment_id}", response_model=GetAssessmentOut)
async def __update_an_assessment(
    assessment_id: int,
    assessment: PatchAssessmentIn,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await update_an_assessment(db_session,
                                        teacher_email=teacher_email,
                                        assessment_id=assessment_id,
                                        assessment_in=assessment)

    if result is None:
        raise HTTPException(404, "assessment doesn't exist!")

    return GetAssessmentOut.from_orm(result)


@router.delete("/{assessment_id}")
async def __delete_an_assessment(
    assessment_id: int,
    teacher_email: str = Depends(verifyUser),
    db_session: AsyncSession = Depends(get_db),
):
    result = await delete_an_assessment(db_session,
                                        teacher_email=teacher_email,
                                        assessment_id=assessment_id)

    if result is None:
        raise HTTPException(404, "assessment doesn't exist!")

    return {'message': 'assessment deleted'}
