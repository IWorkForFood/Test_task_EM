# routers/rbac.py или routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.permissions.dao import RoleDAO, BusinessElementDAO, AccessRuleDAO
from app.permissions.shemas import AccessRuleUpdate, AccessRuleUpdateResponse, Role, BusinessElement
from app.users.dependencies import get_current_user, get_user_permissions_for_resource, permission_required
from .models import AccessRule 
from app.users.models import User

router = APIRouter(
    prefix="/admin/rbac",
    tags=["admin-rbac"],
)

@router.get("/get_roles", response_model = List[Role])
async def get_roles():
    result = await RoleDAO.find_all()
    return result

@router.get("/get_business_element", response_model = List[BusinessElement])
async def get_roles():
    result = await BusinessElementDAO.find_all()
    return result
#admin: User = Depends(permission_required("AccessRule", ["read", "read_all"]))
@router.get(
    "/rules",
    summary="Получить правила доступа (только для админа)"
    )
async def get_roles():
    result = await AccessRuleDAO.find_all()
    return result


@router.patch(
    "/rules",
    response_model=AccessRuleUpdateResponse,
    summary="Обновить правило доступа (только для админа)"
)
async def update_access_rule(
    data: AccessRuleUpdate,
    admin: User = Depends(permission_required("AccessRule", ["update"])),
):
    """
    Обновляет правило доступа по паре role_id + element_id.
    Передаются только те поля, которые нужно изменить (остальные остаются прежними).
    """
    # 1. Проверяем существование роли
    role = await RoleDAO.find_one_or_none(id=data.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")

    # 2. Проверяем существование бизнес-элемента
    element = await BusinessElementDAO.find_one_or_none(id=data.element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Ресурс (business element) не найден")

    # 3. Ищем существующее правило
    rule = await AccessRuleDAO.find_one_or_none(
        role_id=data.role_id,
        element_id=data.element_id
    )

    update_values = data.model_dump(exclude_unset=True, exclude={"role_id", "element_id"})

    if not update_values:
        raise HTTPException(status_code=400, detail="Не переданы поля для обновления")

    if rule:
        # Обновляем существующее правило
        updated_count = await AccessRuleDAO.update(
            filter_by={"id": rule.id},
            **update_values
        )
        if updated_count == 0:
            raise HTTPException(status_code=500, detail="Не удалось обновить правило")

        # Получаем актуальное состояние
        updated_rule = await AccessRuleDAO.find_one_or_none(id=rule.id)
        return updated_rule

    else:
        # Если правила ещё нет — создаём новое
        new_rule = await AccessRuleDAO.add(
            role_id=data.role_id,
            element_id=data.element_id,
            **update_values
        )
        return new_rule
