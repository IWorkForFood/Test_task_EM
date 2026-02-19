from sqlalchemy import select 
from app.database import async_session_maker 
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy import text, insert
from .dao import ReviewDAO
from app.tasks import test_task
from .shemas import SReadReview, SUpdateReview, SCreateReview
import datetime
import os
import time
from app.users.dependencies import get_current_user, permission_required, get_user_permissions_for_resource
from app.users.models import User
from typing import List
from ..products.dao import ProductDAO

router_reviews = APIRouter(prefix='/reviews', tags=['Работа с отзывами'])



@router_reviews.get("/get_product_reviews", response_model=List[SReadReview])
async def get_products(
    product_id: int,
    offset: int, 
    limit: int
):
    all_reviews = await ReviewDAO.find_filtered(product_id=product_id)

    if not all_reviews:
        raise HTTPException(status_code=404, detail="Отзывов на товар нет")


    start = offset
    end = offset + limit
    return all_reviews[start:end]

@router_reviews.post("", response_model=SReadReview, status_code=201)
async def create_product(
    review_data: SCreateReview,
    user: User = Depends(permission_required("Review", ["create"])), 
):
    existing = await ProductDAO.find_one_or_none(id=review_data.product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Данного товара нет")

    is_review = await ReviewDAO.find_one_or_none(product_id=review_data.product_id)
    if is_review:
        raise HTTPException(status_code=409, detail="Отзыв на этот товар от вас уже существует")

    dict_review_data = review_data.dict()
    new_review = await ReviewDAO.add(
        **dict_review_data, user_id = user.id
    )

    return new_review

@router_reviews.patch("/{product_id}", response_model=SReadReview)
async def update_product(
    data: SUpdateReview,
    user: User = Depends(permission_required("Review", ["update", "update_all"])
)):
    review_id = data.id
    review = await ReviewDAO.find_one_or_none(id=review_id)
    if not review:
        raise HTTPException(404, "Комментарий не найден")

    perms = await get_user_permissions_for_resource(user, "Review")

    can_update_all = perms.get("update_all", False)
    can_update_own  = perms.get("update", False)

    if can_update_all:
        pass 

    elif can_update_own:
        if review.user_id != user.id:
            raise HTTPException(403, "Можно редактировать только свои комментарии")
    else:
        raise HTTPException(403, "Нет права на редактирование комментария")

    values = data.model_dump(exclude_unset=True)


    if values:
        updated_count = await ReviewDAO.update(
            filter_by={"id": review_id},
            **values
        )
        if updated_count == 0:
            raise HTTPException(500, "Не удалось обновить товар")

    # Возвращаем актуальное состояние
    updated_review = await ReviewDAO.find_one_or_none(id=review_id)
    return updated_review

@router_reviews.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    user: User = Depends(permission_required("Review", ["delete", "delete_all"])),
):
    review = await ReviewDAO.find_one_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")

    perms = await get_user_permissions_for_resource(user, "Review")
    can_delete_all = perms.get("delete_all", False)
    can_delete_own  = perms.get("delete", False)

    if can_delete_all:
        pass
    elif can_delete_own:
        if review.user_id != user.id:
            raise HTTPException(403, "Можно удалять только свои отзывы")
    else:
        raise HTTPException(403, "Нет права на удаление отзывов")

    deleted = await ReviewDAO.delete_by_id(review_id)
    if not deleted:
        raise HTTPException(500, "Не удалось удалить отзыв")

    return None
