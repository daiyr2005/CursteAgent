from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mysite.api.utils import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
    get_token_data,
    verify_password,
)
from mysite.db.db import get_db
from mysite.db.model import RefreshToken, User
from mysite.db.schema import TokenRead, UserCreate, UserLogin, UserRead, UserUpdate


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)) -> User:
    user_exists = db.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бул email менен пользователь бар",
        )

    user = User(
        full_name=data.full_name,
        email=data.email,
        password=get_password_hash(data.password),
        role=data.role.value,
        is_active=data.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenRead)
def login(data: UserLogin, db: Session = Depends(get_db)) -> TokenRead:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сиз жазган маалымат туура эмес",
        )

    token_data = get_token_data(user)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    db_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(db_token)
    db.commit()

    return TokenRead(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)) -> dict[str, str]:
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маалымат туура эмес")

    db.delete(stored_token)
    db.commit()
    return {"message": "Ийгиликтуу чыкты"}


@router.post("/refresh", response_model=TokenRead)
def refresh(refresh_token: str, db: Session = Depends(get_db)) -> TokenRead:
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Маалымат туура эмес")

    access_token = create_access_token(get_token_data(stored_token.token_user))
    return TokenRead(access_token=access_token)


@router.get("/verify", response_model=UserRead)
def verify_access_token(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/me", response_model=UserRead)
def user_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserRead)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "password" and value is not None:
            value = get_password_hash(value)
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    db.delete(current_user)
    db.commit()
    return {"message": "Аккаунт удалён"}
