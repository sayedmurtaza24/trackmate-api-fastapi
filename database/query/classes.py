from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.query.teachers import find_teacher_by_email
from database.models import Class, Teacher


async def get_class_statistics(db_session: AsyncSession, teacher_email: str, class_id: int):
    query = """
        select count(assessments.id) as total_students,
            count(case when present THEN 1 END) as total_presence,
            count(case when good_perf THEN 1 END) as total_good_perf,
            count(case when good_behave THEN 1 END) as total_good_behave,
            date_part('week', assessments.date) as weeknumber,
            extract(year from assessments.date) as "year"
        from assessments
        join students as st on st.id = assessments.student_id
        join classes as cl on cl.id = st.class_id
        join teachers as te on te.id = cl.teacher_id
        where cl.id = :class_id and te.email = :email
        group by weeknumber, "year"
    """
    count = """
        select count(students.id)
        from students
        join classes as c on c.id = students.class_id
        join teachers as t on t.id = c.teacher_id
        where c.id = :class_id and t.email = :email
    """

    params = {'class_id': class_id, 'email': teacher_email}
    result = await db_session.execute(text(query), params)
    total_students = await db_session.execute(text(count), params)

    return result, total_students.scalar()


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
