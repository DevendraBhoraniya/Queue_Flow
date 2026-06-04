from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.auth import create_access_token
from database.schemas import UserBase, UserLogin, UserResponse, UserLoginResponse
from database.db_user import create_user, get_current_user, get_user, delete_user
from database.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse)
def create(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)

@router.post("/login", response_model=UserLoginResponse)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):

    user = get_user(db, request)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/all", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)    

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id) 

@router.delete("/me")
def delete_me(
    current_user = Depends(get_current_user)
):
    return delete_user(get_db(), current_user.id)
