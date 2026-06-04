from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.schemas import UserBase, UserLogin, UserResponse
from database.db_user import create_user, get_user
from database.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse)
def create(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)

@router.post("/login", response_model=UserResponse)
def login(request: UserLogin, db: Session = Depends(get_db)):
    return get_user(db, request)

