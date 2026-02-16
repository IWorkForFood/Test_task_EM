from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str]
    password: Mapped[str_uniq]
    email: Mapped[str_uniq]
    is_admin: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)

    textreports: Mapped[list['TextReport']] = relationship("TextReport", back_populates="user")

    typical_data: Mapped[list["TypicalData"]] = relationship("TypicalData", back_populates="user")

    extend_existing=True

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"username={self.username!r}")

    def __repr__(self):
        return str(self)



