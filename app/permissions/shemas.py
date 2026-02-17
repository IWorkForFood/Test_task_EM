from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict, field_validator


# ───────────────────────────────────────────────
# Pydantic-схемы (для валидации и OpenAPI)
# ───────────────────────────────────────────────

class AccessRuleBase(BaseModel):
    """Общие поля, используемые в create / update / response"""
    role_id: int = Field(..., ge=1, description="ID роли")
    element_id: int = Field(..., ge=1, description="ID бизнес-объекта / ресурса")

    # Все возможные разрешения — типизированы через Enum
    read: PermissionLevel = Field(default=PermissionLevel.DENY)
    read_all: PermissionLevel = Field(default=PermissionLevel.DENY)
    create: PermissionLevel = Field(default=PermissionLevel.DENY)
    update: PermissionLevel = Field(default=PermissionLevel.DENY)
    update_all: PermissionLevel = Field(default=PermissionLevel.DENY)
    delete: PermissionLevel = Field(default=PermissionLevel.DENY)
    delete_all: PermissionLevel = Field(default=PermissionLevel.DENY)

    model_config = ConfigDict(
        from_attributes=True,          # позволяет работать с ORM-объектами
        json_schema_extra={
            "example": {
                "role_id": 2,
                "element_id": 3,
                "read": "allow",
                "read_all": "deny",
                "create": "allow",
                "update": "allow",
                "update_all": "deny",
                "delete": "allow",
                "delete_all": "deny"
            }
        }
    )


class AccessRuleCreate(AccessRuleBase):
    """Схема для создания новой записи"""
    pass


class AccessRuleUpdate(BaseModel):
    """Схема для частичного обновления — все поля опциональны"""
    role_id: Optional[int] = None
    element_id: Optional[int] = None

    read: Optional[PermissionLevel] = None
    read_all: Optional[PermissionLevel] = None
    create: Optional[PermissionLevel] = None
    update: Optional[PermissionLevel] = None
    update_all: Optional[PermissionLevel] = None
    delete: Optional[PermissionLevel] = None
    delete_all: Optional[PermissionLevel] = None


class AccessRuleOut(AccessRuleBase):
    """Схема для ответа (с id и временными метками)"""
    id: int | uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)





    
    
        



