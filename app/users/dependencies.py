from app.exceptions import TokenNotFound, NoUserIdException, NoJwtException, TokenExpiredException
from fastapi import Request, Depends, HTTPException, status
from .auth_utils import get_auth_data
from .dao import UserDAO 
from jose import jwt, JWTError
from datetime import datetime, timezone
from enum import Enum

def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFound
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        print(f"----- [еее] =======")
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
        
    except JWTError as e:
        print(f"JWT error: {e}")
        raise NoJwtException

    expire: str = payload.get('exp')
    print(f"----- [{expire}] =======")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserDAO.find_one_or_none(id = int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user



