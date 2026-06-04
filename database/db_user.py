from sqlalchemy.orm.session import Session
from database.hash import Hash
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

def get_user(db:Session , request: UserLogin):
    user = db.query(User).filter(User.email == request.email).first()

    if user and Hash.verify(request.password, user.password):
        return user
    return None