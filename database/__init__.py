from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_async_engine(
    settings.db_url,
    future=True,
    echo=True,
)

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator:
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()