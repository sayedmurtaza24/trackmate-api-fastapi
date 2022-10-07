from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import verifyUser
from api.schemas.general import not_found_response 
from api.schemas.classes import GetClassOutOne, PostClassIn, PostClassOut
from database.query.classes import add_a_class, find_class_by_id
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