from fastapi import APIRouter, Depends, Response, HTTPException, status, BackgroundTasks
from sqlalchemy import select 
from app.database import async_session_maker 
from app.users.models import User
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from .auth_utils import get_auth_data, get_password_hash, authenticate_user, create_access_token
from .dependencies import get_current_user
from .models import User
from .shemas import SRegisterUser, SAuthUser
from sqlalchemy import text, insert
from .dao import UserDAO
from app.user_customization.dao import TypicalDataDAO
from pydantic import EmailStr
import uuid
import datetime
import os

router_user = APIRouter(prefix='/users', tags=['Работа с пользовательскими данными'])

async def create_typical_data_for_uset(id: int):
    await TypicalDataDAO.add(user_id = id)

@router_user.post('/registration')
async def add_user(user_data: SRegisterUser, background_tasks: BackgroundTasks):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
        detail='Пользователь c такой почтой уже существует')
    user_dict = user_data.dict()
    user_dict.update({'password': get_password_hash(user_data.password)})
    await UserDAO.add(**user_dict)
    print(user_dict)
    current_user = await UserDAO.find_one_or_none(email=user_dict['email'])
    background_tasks.add_task(create_typical_data_for_uset, current_user.id)
    return {"message": "Вы успешно зарегистрировались!"}

@router_user.post('/login')
async def auth_user(response: Response, uset_data: SAuthUser):
    user = await authenticate_user(**uset_data.dict())
    if not user:
        raise Exception("Пизда!!!")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"ok": True, "access_token": access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}
    
@router_user.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Вы успешно вышли из системы"}

@router_user.get("/me")
async def get_my_data(user_data: User = Depends(get_current_user)):
    return user_data

    
