from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from app.config import settings
from app.users.dao import UserDAO
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=5)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.JWT_KEY, settings.ALGORITHM
    )
    return encode_jwt

async def authenticate_user(email: EmailStr, password:str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user