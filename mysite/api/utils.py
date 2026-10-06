from typing import TypeVar
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from mysite.conf import ACCESS_TOKEN_LIFETIME, ALGORITHM, REFRESH_TOKEN_LIFETIME, SECRET_KEY
from mysite.db.db import get_db
from mysite.db.model import User


ModelType = TypeVar("ModelType")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token туура эмес же мооноту бутту",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_object_or_404(db: Session, model: type[ModelType], object_id: int) -> ModelType:
    db_object = db.get(model, object_id)
    if db_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found",
        )
    return db_object


def create_object(db: Session, model: type[ModelType], data) -> ModelType:
    db_object = model(**data.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


def update_object(db: Session, db_object: ModelType, data) -> ModelType:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_object, field, value)
    db.commit()
    db.refresh(db_object)
    return db_object


def delete_object(db: Session, db_object: object) -> None:
    db.delete(db_object)
    db.commit()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expires = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    )
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY or "change-me", algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


def get_token_data(user: User) -> dict[str, str]:
    return {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY or "change-me", algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user
