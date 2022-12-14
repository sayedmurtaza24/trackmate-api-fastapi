from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Assessment, Class, Teacher, Student
from api.schemas.assessments import PostAssessmentIn
from database.query.students import find_student_by_id


async def add_an_assessment(db_session: AsyncSession,
                            teacher_email: str,
                            student_id: int,
                            assessment: PostAssessmentIn):

    student: Student = await find_student_by_id(db_session, teacher_email, student_id)

    if student is None:
        return None

    no_existing_assessment = (await db_session.execute(
        select(Assessment) \
            .join(Student)
            .where(Student.id == student_id, Assessment.date == assessment.date)
    )).scalars().first()
    
    if no_existing_assessment is not None:
        return False

    new_assessment = Assessment(**assessment.dict())
    student.assessments.append(new_assessment)
    
    db_session.add(student)

    await db_session.commit()

    return new_assessment


async def update_an_assessment(db_session: AsyncSession,
                               teacher_email: str,
                               assessment_id: int,
                               assessment_in: PostAssessmentIn):

    statement = select(Assessment) \
        .join(Student) \
        .join(Class) \
        .join(Teacher) \
        .where(Teacher.email == teacher_email, Assessment.id == assessment_id)

    result = await db_session.execute(statement)

    assessment: Assessment = result.scalars().first()
    
    if assessment is None:
        return None

    assessment.present = assessment_in.present
    assessment.good_perf = assessment_in.good_perf
    assessment.good_behave = assessment_in.good_behave
    assessment.perf_comment = assessment_in.perf_comment
    assessment.behave_comment = assessment_in.behave_comment

    await db_session.flush([assessment])

    return assessment


async def delete_an_assessment(db_session: AsyncSession,
                               teacher_email: str,
                               assessment_id: int):

    statement = select(Assessment) \
        .join(Student) \
        .join(Class) \
        .join(Teacher) \
        .where(Teacher.email == teacher_email, Assessment.id == assessment_id)

    result = await db_session.execute(statement)

    assessment = result.scalars().first()

    if assessment is None:
        return None

    await db_session.delete(assessment)

    return True

