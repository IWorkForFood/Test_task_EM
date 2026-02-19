from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict, field_validator


class AccessRuleUpdate(BaseModel):
    """Схема для обновления одного правила доступа"""
    role_id: int = Field(..., gt=0)
    element_id: int = Field(..., gt=0)

    read: Optional[bool] = None
    read_all: Optional[bool] = None
    create: Optional[bool] = None
    update: Optional[bool] = None
    update_all: Optional[bool] = None
    delete: Optional[bool] = None
    delete_all: Optional[bool] = None

    class Config:
        from_attributes = True

class AccessRuleUpdateResponse(AccessRuleUpdate):
    id: int
    role_id: int
    element_id: int


class Role(BaseModel):
    """Для получения ролей пользователей в системе (admin, seller, buyer, moderator и т.д.)"""

    id: int
    name: str
    description: Optional[str] = None

class BusinessElement(BaseModel):
    """Для получения бизнес-объектов / ресурсов приложений, к которым применяются правила доступа"""
    id: int
    name: str
    description: str


    
    
        



