from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from .dependencies import WorkType

class STextReport(BaseModel):
    id: int = Field(description="id документа")
    filename: str = Field(default="Новый документ", description="Название документа")
    path: str = Field(description="Путь к файлу")
    created_at: datetime = Field(description="Время создания")
    updated_at: datetime = Field(description="Время обновления")

    model_config = ConfigDict(from_attributes=True)

class STextReportUpdate(BaseModel):
    filename: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)



'''
    author_firstname: str
    author_lastname: str
    group_number: str
    record_book_number: str
    department: str
    work_title: str
    instructor_full_name: str
    work_type: WorkType
    completion_year: int
'''