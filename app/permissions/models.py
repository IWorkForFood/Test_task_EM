from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true
from sqlalchemy import UniqueConstraint
from app.users.models import user_roles


class Role(Base):
    """Роли пользователей в системе (admin, seller, buyer, moderator и т.д.)"""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    rules: Mapped[List["AccessRule"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan"
    )

    users: Mapped[list["User"]] = relationship("User", secondary=user_roles, back_populates="roles")


class BusinessElement(Base):
    """Бизнес-объекты / ресурсы приложения, к которым применяются правила доступа"""
    __tablename__ = "business_elements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    rules: Mapped[List["AccessRule"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan"
    )


class AccessRule(Base):
    """Правила доступа: какие действия разрешены конкретной роли для конкретного ресурса"""
    __tablename__ = "access_roles_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    element_id: Mapped[int] = mapped_column(
        ForeignKey("business_elements.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Булевые поля вместо строкового enum
    read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    read_all: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    create: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    update: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    update_all: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    delete_all: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    role: Mapped["Role"] = relationship(back_populates="rules")
    element: Mapped["BusinessElement"] = relationship(back_populates="rules")

    __table_args__ = (
        UniqueConstraint("role_id", "element_id", name="uq_access_rule_role_element"),
    )