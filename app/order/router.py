from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from .shemas import SOrder, SOrderCreate, SOrderUpdate
from .dao import OrderDAO
from ..products.dao import ProductDAO
from ..users.dependencies import get_current_user, permission_required, get_user_permissions_for_resource
from ..users.models import User

router_orders = APIRouter(
    prefix="/orders",
    tags=["Работа с заказами"]
)

@router_orders.get("", response_model=List[SOrder])
async def get_orders(
    limit: int = Query(20, ge=1, le=100, description="Количество на странице"),
    offset: int = Query(0, ge=0, description="Смещение"),
    user: User = Depends(permission_required("Order", ["read", "read_all"])),
):
    perms = await get_user_permissions_for_resource(user, "Order")
    can_read_all = perms.get("read_all", False)

    if can_read_all:
        # Видим все заказы
        orders = await OrderDAO.find_all()
    else:
        # Только свои заказы
        orders = await OrderDAO.find_filtered(buyer_id=user.id)

    # Ручная пагинация (пока DAO не поддерживает offset/limit)
    start = offset
    end = offset + limit
    paginated = orders[start:end]

    if not paginated:
        raise HTTPException(status_code=404, detail="Заказов не найдено")

    return paginated

@router_orders.get("/{order_id}", response_model=SOrder)
async def get_order(
    order_id: int,
    user: User = Depends(permission_required("Order", ["read", "read_all"])),
):
    order = await OrderDAO.find_one_or_none(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    perms = await get_user_permissions_for_resource(user, "Order")
    can_read_all = perms.get("read_all", False)

    if not can_read_all and order.buyer_id != user.id:
        raise HTTPException(403, "Можно просматривать только свои заказы")

    return order

@router_orders.post("", response_model=SOrder, status_code=201)
async def create_order(
    data: SOrderCreate,
    user: User = Depends(permission_required("Order", ["create"])),
):
    # Проверяем существование товара
    product = await ProductDAO.find_one_or_none(id=data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    # Создаём заказ
    new_order = await OrderDAO.add(
        name=data.name,
        cost=data.cost,
        description=data.description,
        buyer_id=user.id,
        product_id=data.product_id,
    )

    return new_order

@router_orders.patch("/{order_id}", response_model=SOrder)
async def update_order(
    order_id: int,
    data: SOrderUpdate,
    user: User = Depends(permission_required("Order", ["update", "update_all"])),
):
    order = await OrderDAO.find_one_or_none(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    perms = await get_user_permissions_for_resource(user, "Order")
    can_update_all = perms.get("update_all", False)
    can_update_own = perms.get("update", False)

    if can_update_all:
        pass  # полный доступ
    elif can_update_own:
        if order.buyer_id != user.id:
            raise HTTPException(403, "Можно редактировать только свои заказы")
    else:
        raise HTTPException(403, "Нет права на редактирование заказов")

    values = data.model_dump(exclude_unset=True)
    if values:
        updated_count = await OrderDAO.update(
            filter_by={"id": order_id},
            **values
        )
        if updated_count == 0:
            raise HTTPException(500, "Не удалось обновить заказ")

    updated_order = await OrderDAO.find_one_or_none(id=order_id)
    return updated_order

@router_orders.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    user: User = Depends(permission_required("Order", ["delete", "delete_all"])),
):
    order = await OrderDAO.find_one_or_none(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    perms = await get_user_permissions_for_resource(user, "Order")
    can_delete_all = perms.get("delete_all", False)
    can_delete_own = perms.get("delete", False)

    if can_delete_all:
        pass  # может удалить любой заказ
    elif can_delete_own:
        if order.buyer_id != user.id:
            raise HTTPException(403, "Можно удалять только свои заказы")
    else:
        raise HTTPException(403, "Нет права на удаление заказов")

    # Удаляем (используем метод delete_by_id из твоего DAO)
    deleted = await OrderDAO.delete_by_id(order_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Не удалось удалить заказ")

    return None