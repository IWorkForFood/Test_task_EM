from sqlalchemy import insert, select
from app.permissions.models import Role, BusinessElement, AccessRule
from app.database import async_session_maker
from app.dao.base import BaseDAO

class RoleDAO(BaseDAO):
    model = Role

class BusinessElementDAO(BaseDAO):
    model = BusinessElement

class AccessRuleDAO(BaseDAO):
    model = AccessRule