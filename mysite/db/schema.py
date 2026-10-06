from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from mysite.db.model import *


class UserBase(BaseModel):
    full_name: str
    email: str
    role: UserRole = UserRole.STUDENT
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenRead(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class RefreshTokenBase(BaseModel):
    user_id: int
    token: str


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenRead(RefreshTokenBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_date: datetime


class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: str | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CourseBase(BaseModel):
    title: str
    category_id: int
    description: str
    level: CourseLevel = CourseLevel.BEGINNER
    price: Decimal = Decimal("0.00")
    duration_weeks: int
    is_active: bool = True
    status: CourseStatus = CourseStatus.FREE


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    category_id: int | None = None
    description: str | None = None
    level: CourseLevel | None = None
    price: Decimal | None = None
    duration_weeks: int | None = None
    is_active: bool | None = None
    status: CourseStatus | None = None


class CourseRead(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class StudyGroupBase(BaseModel):
    name: str
    course_id: int
    teacher_id: int
    starts_on: date
    ends_on: date
    status: GroupStatus = GroupStatus.RECRUITING


class StudyGroupCreate(StudyGroupBase):
    pass


class StudyGroupUpdate(BaseModel):
    name: str | None = None
    course_id: int | None = None
    teacher_id: int | None = None
    starts_on: date | None = None
    ends_on: date | None = None
    status: GroupStatus | None = None


class StudyGroupRead(StudyGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ApplicationBase(BaseModel):
    student_id: int
    course_id: int
    manager_id: int | None = None
    comment: str | None = None
    status: ApplicationStatus = ApplicationStatus.NEW


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    student_id: int | None = None
    course_id: int | None = None
    manager_id: int | None = None
    comment: str | None = None
    status: ApplicationStatus | None = None


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class EnrollmentBase(BaseModel):
    student_id: int
    group_id: int
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    student_id: int | None = None
    group_id: int | None = None
    status: EnrollmentStatus | None = None


class EnrollmentRead(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
