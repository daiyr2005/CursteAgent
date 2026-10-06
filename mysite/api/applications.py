from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from mysite.api.utils import create_object, delete_object, get_object_or_404, update_object
from mysite.db.db import get_db
from mysite.db.model import Application, Course, User
from mysite.db.schema import ApplicationCreate, ApplicationRead, ApplicationUpdate


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)) -> Application:
    get_object_or_404(db, User, data.student_id)
    get_object_or_404(db, Course, data.course_id)
    if data.manager_id is not None:
        get_object_or_404(db, User, data.manager_id)
    return create_object(db, Application, data)


@router.get("", response_model=list[ApplicationRead])
def list_applications(db: Session = Depends(get_db)) -> list[Application]:
    return list(db.scalars(select(Application)).all())


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)) -> Application:
    return get_object_or_404(db, Application, application_id)


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
) -> Application:
    application = get_object_or_404(db, Application, application_id)
    if data.student_id is not None:
        get_object_or_404(db, User, data.student_id)
    if data.course_id is not None:
        get_object_or_404(db, Course, data.course_id)
    if data.manager_id is not None:
        get_object_or_404(db, User, data.manager_id)
    return update_object(db, application, data)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)) -> None:
    application = get_object_or_404(db, Application, application_id)
    delete_object(db, application)
