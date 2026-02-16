from __future__ import annotations
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from enum import Enum

from app.database import Base, str_uniq, int_pk, str_null_true, int_null_true

from sqlalchemy import UniqueConstraint

class PermissionLevel(str, Enum):
    """Уровни разрешений для действий с ресурсами"""
    
    ALLOW = "allow"
    DENY  = "deny"


class Role(Base):
    """Роли пользователей в системе (admin, seller, buyer, moderator и т.д.)"""
    
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    rules: Mapped[List["AccessRuleEnum"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan"
    )


class BusinessElement(Base):
    """Бизнес-объекты / ресурсы приложения, к которым применяются правила доступа
    (User, Product, Order, Review, Category и т.п.)"""
    
    __tablename__ = "business_elements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    rules: Mapped[List["AccessRuleEnum"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan"
    )


class AccessRuleEnum(Base):
    """Правила доступа: какие действия разрешены конкретной роли для конкретного типа ресурса"""
    
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

    read: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    read_all: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    create: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    update: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    update_all: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    delete: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )
    delete_all: Mapped[PermissionLevel] = mapped_column(
        String(10),
        nullable=False,
        default=PermissionLevel.DENY
    )

    role: Mapped["Role"] = relationship(back_populates="rules")
    element: Mapped["BusinessElement"] = relationship(back_populates="rules")

    __table_args__ = (
        UniqueConstraint("role_id", "element_id", name="uq_access_rule_role_element"),
    )