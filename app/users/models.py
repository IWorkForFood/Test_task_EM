from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict

class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str_uniq]
    email: Mapped[str_uniq]
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_seller: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_moderator: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('false'), nullable=False)

    reviews: Mapped[list['Review']] = relationship("Review", back_populates="user")

    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller")

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="buyer")

    extend_existing=True

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"username={self.username!r}")

    def __repr__(self):
        return str(self)



