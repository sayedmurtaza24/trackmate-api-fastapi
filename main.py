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


# eyJhbGciOiJSUzI1NiIsImtpZCI6InRCME0yQSJ9.eyJpc3MiOiJodHRwczovL3Nlc3Npb24uZmlyZWJhc2UuZ29vZ2xlLmNvbS90ZWFjaGVyYXBwLWJiY2JmIiwibmFtZSI6IlNheWVkIE11cnRhemEgTXV0dGFoYXJ5IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BQ05QRXUtNGZ1eldONzZpUHBCX2tXS0N2a0oxTFBKdElmWEFkTm5KbDFUeFx1MDAzZHM5Ni1jIiwiYXVkIjoidGVhY2hlcmFwcC1iYmNiZiIsImF1dGhfdGltZSI6MTY2NTI1MjExMSwidXNlcl9pZCI6IkJXSEp4S1BDWGtPaVg5OEZvRXFEZ0JSdjc4eDIiLCJzdWIiOiJCV0hKeEtQQ1hrT2lYOThGb0VxRGdCUnY3OHgyIiwiaWF0IjoxNjY1MjUyMzY4LCJleHAiOjE2NjU1MTE1NjgsImVtYWlsIjoic2F5ZWRtdXJ0YXphbXV0dGFoYXJ5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA3NjkyOTY1MzUyNjExMDM4NTM0Il0sImVtYWlsIjpbInNheWVkbXVydGF6YW11dHRhaGFyeUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.Ybu0U40ZJzxsQEHtd3tZ-eYLbv1_J2lYvJmNV2TWE21yuv-VKsCXTRinxAoC52Fr5S9AISdpGE8MNo02C20tRsc5HBrrz0sN0G17vvaoQ9q8RDeNDCtqJU_NY9gq7OdKikE-LTWLRwn6KXird2JVVoCYLpkkoqgF4sru49VfiDWMOWX3yDqJr2i1olD_U4HRc6Gxg-znLMvL26lVop960yjKxiA53bsD4Q874re4RNKNq2JKTW4oR_M8M3myJqDCigw361fJUiD7AVo1kuPZlQow1JUpW-bIQXSKvryRhE_XE5htyi7Py6Q31ZHNYipg18SeOYuAL3YeiI1qeQXjEw