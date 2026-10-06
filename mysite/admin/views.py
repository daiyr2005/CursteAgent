from sqladmin import ModelView

from mysite.db.model import *


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.full_name, User.email, User.role, User.is_active]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_date]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.title, Course.category, Course.level, Course.price, Course.status]


class StudyGroupAdmin(ModelView, model=StudyGroup):
    column_list = [StudyGroup.id, StudyGroup.name, StudyGroup.course, StudyGroup.teacher, StudyGroup.status]


class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.id, Application.student, Application.course, Application.status]


class EnrollmentAdmin(ModelView, model=Enrollment):
    column_list = [Enrollment.id, Enrollment.student, Enrollment.group, Enrollment.status]