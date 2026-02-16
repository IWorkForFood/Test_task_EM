from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from .dependencies import WorkType

class STypicalData(BaseModel):

    author_firstname: str | None = Field(default=None)
    author_lastname: str | None = Field(default=None)
    author_surname: str | None = Field(default=None)
    group_number: str | None = Field(default=None)
    record_book_number: str | None = Field(default=None)
    department: str | None = Field(default=None)
    work_title: str | None = Field(default=None)
    instructor_firstname: str | None = Field(default=None)
    instructor_lastname: str | None = Field(default=None)
    instructor_surname: str | None = Field(default=None)
    work_type: WorkType | None = Field(default=None, description="Тип документа")
    completion_year: int | None = Field(default=None)