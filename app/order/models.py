from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict

class Order(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    cost: Mapped[float]
    description: Mapped[str]
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="order")

    buyer: Mapped["User"] = relationship("User", back_populates="orders")

    extend_existing=True

    model_config = ConfigDict(from_attributes=True)
