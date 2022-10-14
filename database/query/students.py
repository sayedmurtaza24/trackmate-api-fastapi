from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from api.schemas.students import PatchStudentIn
from database.query.classes import find_class_by_id
from database.models import Assessment, Class, Teacher, Student


async def find_student_by_id(db_session: AsyncSession, teacher_email: str, student_id: int):
    statement = select(Student) \
        .options(selectinload(Student.assessments)) \
        .join(Class) \
        .join(Teacher) \
        .where(Teacher.email == teacher_email, Student.id == student_id) \

    result = await db_session.execute(statement)

    student = result.scalars().first()

    return student


async def add_a_student(db_session: AsyncSession, 
                        teacher_email: str, 
                        class_id: int, 
                        name: str, 
                        gender: str, 
                        dob: str):
    
    class_ = await find_class_by_id(db_session, teacher_email, class_id)
        
    if class_ is None:
        return None
    
    new_student = Student(name=name, gender=gender, dob=dob, assessments=[])
    class_.students.append(new_student)
    
    db_session.add(class_)
    
    await db_session.commit()
    
    return new_student

async def update_a_student(db_session: AsyncSession,
                           teacher_email: str,
                           student_id: int,
                           student_in: PatchStudentIn):
    
    statement = select(Student) \
        .options(selectinload(Student.assessments)) \
        .join(Class) \
        .join(Teacher) \
        .where(Teacher.email == teacher_email, Student.id == student_id)
        
    result = await db_session.execute(statement)
    
    student = result.scalars().first()
    
    if student is None: return None
    
    student.name = student_in.name
    student.dob = student_in.dob
    student.gender = student_in.gender
    student.emergency_contact_phone = student_in.emergency_contact_phone
    student.emergency_contact_email = student_in.emergency_contact_email
        
    await db_session.flush([student])
    
    return student

async def delete_a_student(db_session: AsyncSession,
                           teacher_email: str,
                           student_id: int):
    
    statement = select(Student) \
        .join(Class) \
        .join(Teacher) \
        .where(Teacher.email == teacher_email, Student.id == student_id)
        
    result = await db_session.execute(statement)
    
    student = result.scalars().first()
    
    if student is None: return None
        
    await db_session.delete(student)
    
    return True