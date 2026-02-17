from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from .dependencies import WorkType

class SOrder(BaseModel):
    id: int = Field(description="id заказа")
    cost: str = Field(default=3, description="Стоимость товара в рублях")
    description: str = Field(description="Описание товара")
    product_name: str = Field(description="Имя товара")
    username: str = Field(description="Имя пользователя, оставившего отзыв")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime = Field(description="Время обновления")

    name: Mapped[str]
    cost: Mapped[float]
    description: Mapped[str]

    model_config = ConfigDict(from_attributes=True)




