from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.query.teachers import find_teacher_by_email
from database.models import Class, Teacher


async def find_class_by_id(db_session: AsyncSession, teacher_email: str, class_id: int):
    statement = select(Class) \
        .options(selectinload(Class.students)) \
        .join(Teacher, Teacher.id == Class.teacher_id) \
        .where(Teacher.email == teacher_email, Class.id == class_id)

    result = await db_session.execute(statement)

    class_ = result.scalars().first()

    return class_


async def add_a_class(db_session: AsyncSession, teacher_email: str, name: str):
    teacher = await find_teacher_by_email(db_session, teacher_email)
        
    if teacher is None:
        return None
    
    new_class = Class(name=name)
    teacher.classes.append(new_class)
    
    db_session.add(teacher)
    
    await db_session.commit()
    
    return new_class
