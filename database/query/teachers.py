from sqlalchemy import insert, select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Teacher
from sqlalchemy.orm import selectinload

async def find_teacher_by_email(db_session: AsyncSession, email: str):
    statement = select(Teacher).options(selectinload(Teacher.classes)).where(Teacher.email == email)
    result: ChunkedIteratorResult = await db_session.execute(statement)
    return result.scalars().first()

async def add_teacher_if_absent(db_session: AsyncSession, name: str, email: str):
    teacher_search = await find_teacher_by_email(db_session, email=email)
    if teacher_search is not None:
        return None
    
    statement = insert(Teacher).values(name=name, email=email).returning(Teacher.id, Teacher.name, Teacher.email)
    result: CursorResult = await db_session.execute(statement)
    await db_session.commit()
    return result.mappings().first()