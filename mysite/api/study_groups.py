from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from mysite.api.utils import create_object, delete_object, get_object_or_404, update_object
from mysite.db.db import get_db
from mysite.db.model import Course, StudyGroup, User
from mysite.db.schema import StudyGroupCreate, StudyGroupRead, StudyGroupUpdate


router = APIRouter(prefix="/study-groups", tags=["study-groups"])


@router.post("", response_model=StudyGroupRead, status_code=status.HTTP_201_CREATED)
def create_study_group(data: StudyGroupCreate, db: Session = Depends(get_db)) -> StudyGroup:
    get_object_or_404(db, Course, data.course_id)
    get_object_or_404(db, User, data.teacher_id)
    return create_object(db, StudyGroup, data)


@router.get("", response_model=list[StudyGroupRead])
def list_study_groups(db: Session = Depends(get_db)) -> list[StudyGroup]:
    return list(db.scalars(select(StudyGroup)).all())


@router.get("/{group_id}", response_model=StudyGroupRead)
def get_study_group(group_id: int, db: Session = Depends(get_db)) -> StudyGroup:
    return get_object_or_404(db, StudyGroup, group_id)


@router.patch("/{group_id}", response_model=StudyGroupRead)
def update_study_group(group_id: int, data: StudyGroupUpdate, db: Session = Depends(get_db)) -> StudyGroup:
    group = get_object_or_404(db, StudyGroup, group_id)
    if data.course_id is not None:
        get_object_or_404(db, Course, data.course_id)
    if data.teacher_id is not None:
        get_object_or_404(db, User, data.teacher_id)
    return update_object(db, group, data)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study_group(group_id: int, db: Session = Depends(get_db)) -> None:
    group = get_object_or_404(db, StudyGroup, group_id)
    delete_object(db, group)
