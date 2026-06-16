from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.auth import create_access_token
from database.schemas import UserBase, UserLogin, UserResponse, UserLoginResponse
from database.db_user import (
    create_user,
    get_current_user,
    get_user,
    delete_user,
    get_all_users as get_all_users_crud,
    get_user_by_id as get_user_by_id_crud,
)
from database.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def create(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)


@router.post("/login", response_model=UserLoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    request = UserLogin(email=form_data.username, password=form_data.password)

    user = get_user(db, request)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})

    return {"user": user, "access_token": access_token, "token_type": "bearer"}


@router.get("/all", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users_crud(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id_crud(db, user_id)


@router.delete("/me")
def delete_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_user(db, current_user.id)
