from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict
from .dependencies import WorkType

class TypicalData(Base):
    id: Mapped[int_pk]
    author_firstname: Mapped[str] = mapped_column(default='Хуба')
    author_lastname: Mapped[str] = mapped_column(default='-')
    author_surname: Mapped[str] = mapped_column(default='Буба')
    group_number: Mapped[str] = mapped_column(default='КИ18-14/2ю')
    record_book_number: Mapped[str] = mapped_column(default='032322108')
    department: Mapped[str] = mapped_column(default='Лютая сварка')
    work_title: Mapped[str] = mapped_column(default='Наркобизнес в технологических системах')
    instructor_firstname: Mapped[str] = mapped_column(default='Зубенко')
    instructor_lastname: Mapped[str] = mapped_column(default='Михаил')
    instructor_surname: Mapped[str] = mapped_column(default='Петрович')
    work_type: Mapped[WorkType] = mapped_column(default='practical_work_report')
    completion_year: Mapped[int] = mapped_column(default=2025)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="typical_data")

    extend_existing=True

    model_config = ConfigDict(from_attributes=True)

