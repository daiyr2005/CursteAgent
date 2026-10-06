from fastapi import FastAPI
from sqladmin import Admin

from mysite.db.db import engine

from .views import (
    ApplicationAdmin,
    CategoryAdmin,
    CourseAdmin,
    EnrollmentAdmin,
    RefreshTokenAdmin,
    StudyGroupAdmin,
    UserAdmin,
)


def setup_admin(user_app: FastAPI):
    admin = Admin(user_app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(StudyGroupAdmin)
    admin.add_view(ApplicationAdmin)
    admin.add_view(EnrollmentAdmin)