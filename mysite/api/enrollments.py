from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from mysite.api.utils import create_object, delete_object, get_object_or_404, update_object
from mysite.db.db import get_db
from mysite.db.model import Enrollment, StudyGroup, User
from mysite.db.schema import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate


router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db)) -> Enrollment:
    get_object_or_404(db, User, data.student_id)
    get_object_or_404(db, StudyGroup, data.group_id)
    return create_object(db, Enrollment, data)


@router.get("", response_model=list[EnrollmentRead])
def list_enrollments(db: Session = Depends(get_db)) -> list[Enrollment]:
    return list(db.scalars(select(Enrollment)).all())


@router.get("/{enrollment_id}", response_model=EnrollmentRead)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)) -> Enrollment:
    return get_object_or_404(db, Enrollment, enrollment_id)


@router.patch("/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(enrollment_id: int, data: EnrollmentUpdate, db: Session = Depends(get_db)) -> Enrollment:
    enrollment = get_object_or_404(db, Enrollment, enrollment_id)
    if data.student_id is not None:
        get_object_or_404(db, User, data.student_id)
    if data.group_id is not None:
        get_object_or_404(db, StudyGroup, data.group_id)
    return update_object(db, enrollment, data)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)) -> None:
    enrollment = get_object_or_404(db, Enrollment, enrollment_id)
    delete_object(db, enrollment)
