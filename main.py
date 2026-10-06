from fastapi import FastAPI

from mysite.api.applications import router as applications_router
from mysite.api.auth import router as auth_router
from mysite.api.categories import router as categories_router
from mysite.api.courses import router as courses_router
from mysite.api.enrollments import router as enrollments_router
from mysite.api.refresh_tokens import router as refresh_tokens_router
from mysite.api.study_groups import router as study_groups_router
from mysite.api.users import router as users_router
from mysite.db.db import Base, engine


app = FastAPI(title="Course API")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Course API is running"}


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(refresh_tokens_router)
app.include_router(categories_router)
app.include_router(courses_router)
app.include_router(study_groups_router)
app.include_router(applications_router)
app.include_router(enrollments_router)
