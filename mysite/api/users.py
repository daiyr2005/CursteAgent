from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from mysite.api.utils import create_object, delete_object, get_object_or_404, update_object
from mysite.db.db import get_db
from mysite.db.model import User
from mysite.db.schema import UserCreate, UserRead, UserUpdate
from mysite.db.model import RefreshToken, User
from mysite.db.schema import RefreshTokenCreate, RefreshTokenRead


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)) -> User:
    return create_object(db, User, data)


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return list(db.scalars(select(User)).all())


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    return get_object_or_404(db, User, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)) -> User:
    user = get_object_or_404(db, User, user_id)
    return update_object(db, user, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user = get_object_or_404(db, User, user_id)
    delete_object(db, user)


@router.post("", response_model=RefreshTokenRead, status_code=status.HTTP_201_CREATED)
def create_refresh_token(data: RefreshTokenCreate, db: Session = Depends(get_db)) -> RefreshToken:
    get_object_or_404(db, User, data.user_id)
    return create_object(db, RefreshToken, data)


@router.get("", response_model=list[RefreshTokenRead])
def list_refresh_tokens(db: Session = Depends(get_db)) -> list[RefreshToken]:
    return list(db.scalars(select(RefreshToken)).all())


@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refresh_token(token_id: int, db: Session = Depends(get_db)) -> None:
    token = get_object_or_404(db, RefreshToken, token_id)
    delete_object(db, token)
