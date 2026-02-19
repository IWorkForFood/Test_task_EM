from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict, field_validator
from .dependencies import ProductCategory
from app.database import int_pk

class SProduct(BaseModel):
    id: int_pk
    sku: str
    name: str
    description: str
    price: float = Field(description="Цена на товар")
    stock: int = Field(description="Кол-во товаров в наличии")
    contact_phone: str = Field(description="Номер телефона")
    
    category: ProductCategory

    model_config = ConfigDict(from_attributes=True)


class SCreateProduct(BaseModel):

    name: str = Field(min_length=1, max_length=20)
    description: str = Field(max_length=1000)
    price: float = Field(description="Цена на товар")
    stock: int = Field(description="Кол-во товаров в наличии")
    contact_phone: str = Field(description="Номер телефона")
    
    category: ProductCategory

    model_config = ConfigDict(from_attributes=True)

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Количество товаров не может быть меньше нуля")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Цена должна быть больше нуля")
        return v
    
    @field_validator("contact_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Убираем пробелы, скобки, тире
        cleaned = re.sub(r'[\s\-\(\)]', '', v)

        # Приводим к единому формату
        if cleaned.startswith('8'):
            cleaned = '+7' + cleaned[1:]
        elif cleaned.startswith('7') and len(cleaned) == 11:
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+'):
            cleaned = '+7' + cleaned

        # Самый простой и надёжный паттерн для РФ номера
        if not re.match(r'^\+7\d{10}$', cleaned):
            raise ValueError("Номер телефона должен быть в формате +7XXXXXXXXXX")

        return cleaned


class SUpdateProduct(SCreateProduct):
    pass


