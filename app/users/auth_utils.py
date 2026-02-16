from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.config import get_auth_data
from pydantic import EmailStr
from .dao import UserDAO
from jose import jwt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(30)
    to_encode.update({"exp": expire_time})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    print(f"/n/n//n/n/n//n/n {user.password} /n {get_password_hash(password)} /n {verify_password(user.password, get_password_hash(password))}   /nn/n//n/n/n//n/n/n//n//n/n/n/n/n/n/n/nn//n/n/n//n/n/n/n/n/ ")
    if user and verify_password(plain_password=password, hashed_password=user.password):
        return user
    return None





