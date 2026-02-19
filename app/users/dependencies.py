from app.exceptions import TokenNotFound, NoUserIdException, NoJwtException, TokenExpiredException
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import Request, Depends, HTTPException, status
from .auth_utils import get_auth_data
from .dao import UserDAO 
from jose import jwt, JWTError
from datetime import datetime, timezone
from enum import Enum
from app.database import async_session_maker
from app.users.models import User
from app.permissions.models import Role, AccessRule
from typing import Dict, List

import logging

def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFound
    return token

async def get_current_user(
    token: str = Depends(get_token),
):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError as e:
        print(f"JWT error: {e}")
        raise NoJwtException

    expire = payload.get('exp')
    if not expire or datetime.fromtimestamp(int(expire), tz=timezone.utc) < datetime.now(timezone.utc):
        raise TokenExpiredException

    user_id_str = payload.get('sub')
    if not user_id_str:
        raise NoUserIdException

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(401, "Invalid user id")

    # Предзагружаем роли + правила + элемент
    stmt = (
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.rules).selectinload(AccessRule.element)
        )
        .where(User.id == user_id)
    )

    async with async_session_maker() as session:
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is inactive")

    return user


async def get_user_permissions_for_resource(
    user: User,
    resource_name: str  # "Product", "Order" etc.
) -> Dict[str, bool]:
    """
    Динамически получает объединённые права для ресурса.
    Возвращает: {"read": True, "create": False, ...}
    """
    permissions = {
        "read": False, "read_all": False,
        "create": False,
        "update": False, "update_all": False,
        "delete": False, "delete_all": False,
    }

    if not user.roles:
        return permissions

    for role in user.roles:  # перебор ролей динамически
        for rule in role.rules:  # перебор разрешений роли
            if rule.element.name == resource_name:  # матчим по имени ресурса
                permissions["read"] = permissions["read"] or rule.read
                permissions["read_all"] = permissions["read_all"] or rule.read_all
                permissions["create"] = permissions["create"] or rule.create
                permissions["update"] = permissions["update"] or rule.update
                permissions["update_all"] = permissions["update_all"] or rule.update_all
                permissions["delete"] = permissions["delete"] or rule.delete
                permissions["delete_all"] = permissions["delete_all"] or rule.delete_all
    
    print(permissions)
    logging.warning(permissions)

    return permissions

def permission_required(resource: str, actions: List[str]):
    async def dependency(user: User = Depends(get_current_user)):
        perms = await get_user_permissions_for_resource(user, resource)
        if not any(perms.get(a, False) for a in actions):
            raise HTTPException(
                status_code=403,
                detail=f"Нет ни одного из прав {actions} на ресурс '{resource}'"
            )
        return user
    return dependency