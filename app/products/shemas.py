from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from .dependencies import WorkType

class STextReport(BaseModel):
    id: int = Field(description="id отзыва")
    stars_amount: int = Field(default=3, description="Кол-во звезд (оценка товара)")
    review_content: str = Field(description="Содержание отзыва")
    username: str = Field(description="Имя пользователя, оставившего отзыв")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime = Field(description="Время обновления")

    model_config = ConfigDict(from_attributes=True)



