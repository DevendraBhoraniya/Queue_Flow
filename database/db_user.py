from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from auth.auth import Hash, verify_token
from database.database import get_db
from database.models import User
from database.schemas import UserBase, UserLogin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_user(db: Session, request: UserBase):
    new_user = User(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, request: UserLogin):
    user = db.query(User).filter(User.email == request.email).first()

    if user and Hash.verify(request.password, user.password):
        return user

    return None


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user_id = verify_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(db, int(user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return "User deleted successfully"
    return "User not found, deletion failed, please check the user ID and try again"
