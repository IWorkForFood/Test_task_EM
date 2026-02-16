from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict

class Review(Base):
    id: Mapped[int_pk]
    stars_amount: Mapped[int]
    title: Mapped[str]
    review_content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, unique=True)

    user: Mapped["User"] = relationship("User", back_populates="reviews")

    extend_existing=True

    model_config = ConfigDict(from_attributes=True)


