from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select 
from app.database import async_session_maker 
from app.users.models import User
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import text, insert
from .dao import TypicalDataDAO
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from .shemas import STypicalData
import uuid
import datetime
import os

router_user_customization = APIRouter(prefix='/custom_settings', tags=['Работа с типичными настройками'])

@router_user_customization.patch('/set_typical_data')
async def change_user_customization(values: STypicalData, user_data: User = Depends(get_current_user)):
    
    print(user_data.id)
    existing = await TypicalDataDAO.find_one_or_none(user_id=user_data.id)
    if not existing:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    dict_values = values.dict(exclude_unset=True)  # ← лучше использовать exclude_unset
    updated_rows = await TypicalDataDAO.update({"user_id": user_data.id}, **dict_values)
    
    if updated_rows == 0:
        raise HTTPException(status_code=400, detail="Не удалось обновить запись")
    
    return {"message": "Шаблонные данные успешно обновлены"}

    

