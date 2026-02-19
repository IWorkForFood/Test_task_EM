from datetime import datetime, date
from typing import Optional
import re
from ..database import int_pk 
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict

class SCreateReview(BaseModel):
    stars_amount: int = Field(ge=0, le=10, default=3, description="Кол-во звезд (оценка товара)")
    review_content: str = Field(description="Содержание отзыва")
    title: str
    product_id: int = Field(description="Имя пользователя, оставившего отзыв")

class SUpdateReview(BaseModel):
    id: int_pk
    stars_amount: int = Field(ge=0, le=10, default=3, description="Кол-во звезд (оценка товара)")
    review_content: str = Field(description="Содержание отзыва")
    title: str

class SReadReview(SCreateReview):
    id: int = Field(description="id объявления")
    #username: str = Field(description="Имя пользователя, оставившего отзыв")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime = Field(description="Время обновления")



