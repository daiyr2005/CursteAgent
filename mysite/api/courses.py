from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from mysite.api.utils import create_object, delete_object, get_object_or_404, update_object
from mysite.db.db import get_db
from mysite.db.model import Category, Course
from mysite.db.schema import CourseCreate, CourseRead, CourseUpdate


router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, db: Session = Depends(get_db)) -> Course:
    get_object_or_404(db, Category, data.category_id)
    return create_object(db, Course, data)


@router.get("", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)) -> list[Course]:
    return list(db.scalars(select(Course)).all())


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)) -> Course:
    return get_object_or_404(db, Course, course_id)


@router.patch("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db)) -> Course:
    course = get_object_or_404(db, Course, course_id)
    if data.category_id is not None:
        get_object_or_404(db, Category, data.category_id)
    return update_object(db, course, data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)) -> None:
    course = get_object_or_404(db, Course, course_id)
    delete_object(db, course)
