from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from database.auth import Hash , verify_token
from database.database import get_db
from database.models import User
from database.schemas import UserBase, UserLogin

def create_user(db: Session , request: UserBase):
    new_user = User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, request: UserLogin):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if user and Hash.verify(
        request.password,
        user.password
    ):
        return user

    return None

def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)

    user = get_user_by_id(
        db,
        user_id
    )

    return user

def get_user_by_id(db:Session , user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db:Session):
    return db.query(User).all()

def delete_user(db:Session , user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return "User deleted successfully"
    return "User not found, deletion failed, please check the user ID and try again"