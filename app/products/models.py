from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from datetime import date
from enum import Enum
from pydantic import field_validator, ValidationError, ConfigDict
from .dependencies import ProductCategory
from sqlalchemy import String, Integer, ForeignKey, func, DateTime

class Product(Base):
    id: Mapped[int_pk]
    sku: Mapped[str] = mapped_column(
        String(64),          
        unique=True,        
        nullable=False,     
        index=True       
    )

    name: Mapped[str]
    description: Mapped[str]
    sku: Mapped[int]
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(default=0)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    contact_phone: Mapped[str]
    
    category: Mapped[ProductCategory]

    order: Mapped["Order"] = relationship("Order", back_populates="product")

    seller: Mapped["User"] = relationship("User", back_populates="products")

    #user: Mapped["User"] = relationship("User", back_populates="textreports")
    extend_existing=True

    model_config = ConfigDict(from_attributes=True)

