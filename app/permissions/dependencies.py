from enum import Enum

class PermissionLevel(str, Enum):
    """Уровень доступа для конкретного действия"""
    ALLOW = "allow"
    DENY = "deny"
    # можно добавить OWNER_ONLY = "owner_only" если захочешь ещё более тонкую настройку


class ActionType(str, Enum):
    """Тип действия, для которого задаётся разрешение"""
    READ       = "read"
    READ_ALL   = "read_all"
    CREATE     = "create"
    UPDATE     = "update"
    UPDATE_ALL = "update_all"
    DELETE     = "delete"
    DELETE_ALL = "delete_all"


