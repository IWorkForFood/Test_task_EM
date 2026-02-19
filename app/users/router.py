from fastapi import APIRouter, Depends, Response, HTTPException, status, BackgroundTasks
from sqlalchemy import select 
from app.database import async_session_maker 
from app.users.models import User
from app.permissions.models import Role
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from .auth_utils import get_auth_data, get_password_hash, authenticate_user, create_access_token
from .dependencies import get_current_user
from .models import User, user_roles
from .shemas import SRegisterUser, SAuthUser, SEditUserData
from sqlalchemy import text, insert
from .dao import UserDAO
from pydantic import EmailStr
from app.exceptions import TokenExpiredException
import uuid
import datetime
import os

router_user = APIRouter(prefix='/users', tags=['Работа с пользовательскими данными'])


@router_user.post('/registration')
async def add_user(user_data: SRegisterUser, background_tasks: BackgroundTasks):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
        detail='Пользователь c такой почтой уже существует')
    user_dict = user_data.dict()
    del user_dict['password_replay']
    del user_dict['role_ids']
    user_dict.update({'password': get_password_hash(user_data.password)})
    await UserDAO.add(**user_dict)
    current_user = await UserDAO.find_one_or_none(email=user_dict['email'])

    async with async_session_maker() as session:

        if user_data.role_ids:
            # Проверяем, что роли существуют
            roles = await session.execute(
                select(Role).where(Role.id.in_(user_data.role_ids))
            )
            existing_roles = roles.scalars().all()
            
            if len(existing_roles) != len(user_data.role_ids):
                raise HTTPException(400, "Одна или несколько ролей не найдены")

            # Добавляем связи
            for role_id in user_data.role_ids:
                # Можно добавить через insert в user_roles
                await session.execute(
                    user_roles.insert().values(user_id=current_user.id, role_id=role_id)
                )

        await session.commit()

    return {"message": "Вы успешно зарегистрировались!"}

@router_user.post('/login')
async def auth_user(response: Response, uset_data: SAuthUser):
    user = await authenticate_user(**uset_data.dict())
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Неверные учётные данные ')
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

@router_user.patch("/update")
async def update_my_data(data_for_update: SEditUserData, user_data: User = Depends(get_current_user)):
    dict_data_for_update = data_for_update.model_dump(exclude_unset=True)
    result = await UserDAO.update(filter_by={"id": user_data.id}, **dict_data_for_update)
    return {"message": "Данные успешно обновлены"}

@router_user.delete("/delete_account")
async def delete_account(response: Response, user_data: User = Depends(get_current_user)):
    response.delete_cookie(key="users_access_token")
    result = await UserDAO.update(filter_by={"id": user_data.id}, is_active = False)
    return {"message": "Аккаунт был удален"}