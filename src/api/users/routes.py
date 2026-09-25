import bcrypt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import getdb
from .models import User
from .schemas import CreateUserRequest, UserResponse, LoginRequest, TokenResponse
from fastapi import HTTPException, status
from .auth import create_access_token

user_router = APIRouter(tags=["USERS"])


@user_router.post("/create-user", response_model=UserResponse)
def create_user(
    payload: CreateUserRequest,
    db: Session = Depends(getdb),
):
    hashed_password = bcrypt.hashpw(
        payload.password.encode(),
        bcrypt.gensalt(),
    ).decode()

    print("PAYLOAD SCOPE:", payload.scope)

    new_user = User(
        name=payload.name,
        password=hashed_password,
        scope=payload.scope,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(getdb),
):
    user = db.query(User).filter(User.name == payload.name).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not bcrypt.checkpw(
        payload.password.encode(),
        user.password.encode(),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    scopes = user.scope.split()

    token = create_access_token(
        str(user.user_id),
        scopes,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }