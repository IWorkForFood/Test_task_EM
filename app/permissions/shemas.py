from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict, field_validator


class SAuthUser(BaseModel):
    email: str = Field(description="Электронная почта студента")
    password: str = Field(min_length=6, max_length=30)

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str):
        if not re.match("(?=.*[0-9])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}", value):
            raise ValueError("Пароль должен содержать хотя бы 1 заглавную латинскую букву, хотя бы 1 цифру")
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str):
        if not re.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Невалидный email")
        return value

class SRegisterUser(SAuthUser):
    username: str = Field(..., min_length=1, max_length=30)



    
    
        



