from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

pwd_ctx = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# For Hasing and Verifying Passwords
class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        return pwd_ctx.verify(plain_password, hashed_password)
    
# For Creating and Verifying JWT Tokens
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None