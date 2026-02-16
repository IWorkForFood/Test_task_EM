from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict
from .dependencies import WorkType

class TextReport(Base):
    id: Mapped[int_pk]
    filename: Mapped[str]
    path: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="textreports")

    extend_existing=True

    model_config = ConfigDict(from_attributes=True)



