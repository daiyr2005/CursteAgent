import uvicorn
from fastapi import FastAPI

from mysite.admin.setup import setup_admin
from mysite.api import (
    applications,
    auth,
    categories,
    courses,
    enrollments,
    study_groups,
    users,
)

app = FastAPI(title="Courses API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(courses.router)
app.include_router(study_groups.router)
app.include_router(applications.router)
app.include_router(enrollments.router)

setup_admin(app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)