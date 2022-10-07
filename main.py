from fastapi import Depends, FastAPI
from api import teachers, classes, auth, students, assessments
from config import settings
from database import engine
from database.models import Base
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, UJSONResponse
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
    responses={**validation_error_response, **login_fail_response})


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

@app.get("/b")
async def __for_benchmark():
    return UJSONResponse({'message': 'hi'}, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.host,
                port=int(settings.port),
                reload=True)


# eyJhbGciOiJSUzI1NiIsImtpZCI6InRCME0yQSJ9.eyJpc3MiOiJodHRwczovL3Nlc3Npb24uZmlyZWJhc2UuZ29vZ2xlLmNvbS90ZWFjaGVyYXBwLWJiY2JmIiwibmFtZSI6IlNheWVkIE11cnRhemEgTXV0dGFoYXJ5IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BQ05QRXUtNGZ1eldONzZpUHBCX2tXS0N2a0oxTFBKdElmWEFkTm5KbDFUeFx1MDAzZHM5Ni1jIiwiYXVkIjoidGVhY2hlcmFwcC1iYmNiZiIsImF1dGhfdGltZSI6MTY2NDk5MTE0MCwidXNlcl9pZCI6IkJXSEp4S1BDWGtPaVg5OEZvRXFEZ0JSdjc4eDIiLCJzdWIiOiJCV0hKeEtQQ1hrT2lYOThGb0VxRGdCUnY3OHgyIiwiaWF0IjoxNjY0OTkxMTQ4LCJleHAiOjE2NjUyNTAzNDgsImVtYWlsIjoic2F5ZWRtdXJ0YXphbXV0dGFoYXJ5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA3NjkyOTY1MzUyNjExMDM4NTM0Il0sImVtYWlsIjpbInNheWVkbXVydGF6YW11dHRhaGFyeUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.DPbKwtZr6rhGC9Sb256zZKg_VZsIZEh4E-UQY4MiEObj4VWnSReUW-c-b4NjwMTXA0HHWOXr6gFDglv0MoT1g61zZu5bf__NmlynKjMLGhWu5uDFR9jM4JDOgIaaCmQ3epMFg8F3XL-qjB0iiYvvR3TA8d5Vb8nGzK6rV56fgsd8EZg6GO08B9dUhezSRK_h3XohaacAutesTBXaYYjVTp8MT82ZaGVCnn5F1FbCAIX5ikmKjN4tchBbKT--8vMIPw0eL-DHb--OJAnWl5VfXFHZN8z1ulb6izwVMzmzbAprhfmf2RLu7aUXsUSNJ4lGk_hB2T3xxabAeaHw_M2HsA
