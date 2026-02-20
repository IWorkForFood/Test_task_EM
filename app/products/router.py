from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from .shemas import SProduct, SCreateProduct, SUpdateProduct, ProductCategory
from .dao import ProductDAO
from ..users.dependencies import get_current_user  
from ..users.models import User
from ..users.dependencies import permission_required, get_user_permissions_for_resource

import uuid
import re

products_router = APIRouter(
    prefix="/products",
    tags=["Работа с объявлениями"]
)


def generate_sku(name: str) -> str:
    """Генерация SKU: 3–4 символа из названия + 8 символов uuid"""
    clean = re.sub(r'[^A-Z0-9]', '', name.upper())[:4]
    if len(clean) < 3:
        clean = (clean + "ITEM")[:4]
    uuid_part = str(uuid.uuid4()).replace("-", "")[:8]
    return f"{clean}-{uuid_part}"


def validate_phone(phone: str) -> str:
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    if cleaned.startswith('8'):
        cleaned = '7' + cleaned[1:]
    if not cleaned.startswith('7'):
        cleaned = '7' + cleaned
    if len(cleaned) != 11 or not cleaned.isdigit():
        raise ValueError("Номер должен быть российским в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
    return f"+7{cleaned[1:]}"


@products_router.get("", response_model=List[SProduct])
async def get_products(
    limit: int = 20,
    offset: int = 0,
    category: Optional[ProductCategory] = None
):

    all_products = await ProductDAO.find_all()

    # Ручная пагинация и фильтр (временное решение)
    if category:
        all_products = [p for p in all_products if p.category == category]

    start = offset
    end = offset + limit
    return all_products[start:end]


@products_router.get("/{product_id}", response_model=SProduct)
async def get_product(product_id: int):
    product = await ProductDAO.find_one_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@products_router.post("", response_model=SProduct, status_code=201)
async def create_product(
    data: SCreateProduct,
    user: User = Depends(permission_required("Product", ["create"]))
):
    try:
        phone = validate_phone(data.contact_phone)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if data.price < 0:
        raise HTTPException(422, "Цена не может быть отрицательной")
    if data.stock < 0:
        raise HTTPException(422, "Количество не может быть отрицательным")

    sku = generate_sku(data.name)

    # Проверка на коллизию SKU (в production лучше делать unique constraint + try/except)
    existing = await ProductDAO.find_one_or_none(sku=sku)
    if existing:
        sku = generate_sku(data.name + str(uuid.uuid4())[:5])

    new_product = await ProductDAO.add(
        sku=sku,
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        contact_phone=phone,
        category=data.category,
        seller_id=user.id,
    )

    return new_product


@products_router.patch("/{product_id}", response_model=SProduct)
async def update_product(
    product_id: int,
    data: SUpdateProduct,
    user: User = Depends(permission_required("Product", ["update", "update_all"])
)):
    product = await ProductDAO.find_one_or_none(id=product_id)
    if not product:
        raise HTTPException(404, "Товар не найден")

    perms = await get_user_permissions_for_resource(user, "Product")

    can_update_all = perms.get("update_all", False)
    can_update_own  = perms.get("update", False)

    # Если есть update_all → можно редактировать любой товар
    if can_update_all:
        pass  # полный доступ — ничего не проверяем

    # Иначе — только свой товар
    elif can_update_own:
        if product.seller_id != user.id:
            raise HTTPException(403, "Можно редактировать только свои товары")
    else:
        raise HTTPException(403, "Нет права на редактирование товаров")

    values = data.model_dump(exclude_unset=True)

    if "contact_phone" in values:
        try:
            values["contact_phone"] = validate_phone(values["contact_phone"])
        except ValueError as e:
            raise HTTPException(422, str(e))

    if values:
        updated_count = await ProductDAO.update(
            filter_by={"id": product_id},
            **values
        )
        if updated_count == 0:
            raise HTTPException(500, "Не удалось обновить товар")

    # Возвращаем актуальное состояние
    updated_product = await ProductDAO.find_one_or_none(id=product_id)
    return updated_product


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    user: User = Depends(permission_required("Product", ["delete", "delete_all"])),
):
    product = await ProductDAO.find_one_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    perms = await get_user_permissions_for_resource(user, "Product")
    can_delete_all = perms.get("delete_all", False)
    can_delete_own  = perms.get("delete", False)

    if can_delete_all:
        pass  
    elif can_delete_own:
        if product.seller_id != user.id:
            raise HTTPException(403, "Можно удалять только свои товары")
    else:
        raise HTTPException(403, "Нет права на удаление товаров")

    deleted = await ProductDAO.delete_by_id(product_id)  
    if not deleted:
        raise HTTPException(500, "Не удалось удалить товар")

    # Возвращаем 204 No Content при успешном удалении
    return None

