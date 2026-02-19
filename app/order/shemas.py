from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SOrder(BaseModel):
    """Схема заказа (ответ)"""
    id: int = Field(description="ID заказа")
    name: str = Field(description="Название заказа")
    cost: float = Field(description="Стоимость в рублях")
    description: str = Field(description="Описание заказа")
    buyer_id: int = Field(description="ID покупателя")
    product_id: int = Field(description="ID товара")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime = Field(description="Время обновления")

    model_config = ConfigDict(from_attributes=True)


class SOrderCreate(BaseModel):
    """Схема создания заказа"""
    name: str = Field(min_length=1, max_length=100, description="Название заказа")
    cost: float = Field(gt=0, description="Стоимость в рублях (> 0)")
    description: str = Field(max_length=1000, description="Описание заказа")
    product_id: int = Field(gt=0, description="ID товара")


class SOrderUpdate(BaseModel):
    """Схема обновления заказа (все поля опциональны)"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    cost: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, max_length=1000)
    product_id: Optional[int] = Field(default=None, gt=0)


class SOrderReadMinimal(BaseModel):
    """Минимальная схема заказа для списков"""
    id: int
    name: str
    cost: float
    buyer_id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)