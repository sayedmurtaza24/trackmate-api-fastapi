from fastapi import FastAPI
from api import teachers, classes, auth, students, assessments
from config import settings
from database import engine
from database.models import Base
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from api.schemas.general import validation_error_response, login_fail_response, ValidationError
import uvicorn

app = FastAPI(
    title="TrackMate API",
    description="""A RESTful API for managing students presence, 
                   academic performance and academic behavior in schools.""",
    version="1.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    responses={**validation_error_response,
               **login_fail_response})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, __):
    return UJSONResponse(ValidationError().dict(), status_code=403)


@app.on_event('startup')
async def init_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        await conn.close()

app.include_router(auth.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(students.router)
app.include_router(assessments.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.host,
                port=int(settings.port),
                reload=True)
