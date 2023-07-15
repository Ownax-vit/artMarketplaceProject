from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User
from src.marketplace.models import BasketItem
from src.marketplace.schemas.basket import Basket, CreateBasketItem, \
    UpdateBasketItem, ResponseBasketItem
from src.auth.dependencies import get_current_user_authorizer
from src.marketplace.utils import basket_item_to_schema

router = APIRouter(tags=["basket"])


@router.get("/basket",  tags=["basket"],
            response_model=Basket,
            status_code=status.HTTP_200_OK)
async def get_basket_items(user: User = Depends(get_current_user_authorizer()),
                           session: AsyncSession = Depends(get_async_session)):
    """ Вывод состава корзины пользователя, пользователь идентифицируется по токену"""

    res = await BasketItem.get_all_products(session, user.id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Products in basket not found")

    list_basket_item = []
    count = 0
    sum_price_basker = 0
    for basket_item in res:
        base_basket_item = basket_item_to_schema(basket_item)
        count += base_basket_item.count
        sum_price_basker += base_basket_item.sum_price
        list_basket_item.append(base_basket_item)

    return Basket(count=count, sum=sum_price_basker, list_products=list_basket_item)


@router.post("/basket",  tags=["basket"],
             response_model=ResponseBasketItem,
             status_code=status.HTTP_201_CREATED)
async def add_item_to_basket(basket_item: CreateBasketItem,
                             user: User = Depends(get_current_user_authorizer()),
                             session: AsyncSession = Depends(get_async_session)):
    """ Добавить товар в корзину """
    basket_model = BasketItem(product_id=basket_item.product_id,
                              user_id=user.id,
                              count=basket_item.count)
    try:
        await basket_model.save(session)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Incorrect data or method, check if product in basket for user")
    return ResponseBasketItem(**basket_item.model_dump(), user_id=user.id)


@router.patch("/basket/{product_id}",  tags=["basket"],
              response_model=ResponseBasketItem,
              status_code=status.HTTP_200_OK)
async def update_item_in_basket(product_id: UUID,
                                basket_item: UpdateBasketItem,
                                user: User = Depends(get_current_user_authorizer()),
                                session: AsyncSession = Depends(get_async_session)):
    item = await BasketItem.find(session, product_id, user.id)

    try:
        await item.update(session, count=basket_item.count)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Incorrect data or method")

    return ResponseBasketItem(**basket_item.model_dump(), user_id=user.id, product_id=item.product_id)


@router.delete("/basket/{product_id}",  tags=["basket"],
               response_model=ResponseBasketItem,
               status_code=status.HTTP_200_OK)
async def delete_item_from_basket(product_id: UUID,
                                  user: User = Depends(get_current_user_authorizer()),
                                  session: AsyncSession = Depends(get_async_session)):
    item = await BasketItem.find(session, product_id, user.id)
    try:
        await item.delete(session)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Incorrect data or method")
    return ResponseBasketItem(user_id=user.id, product_id=item.product_id, count=item.count)


@router.delete("/basket_clear", tags=["basket"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_items_from_basket(user: User = Depends(get_current_user_authorizer()),
                                       session: AsyncSession = Depends(get_async_session)):

    return await BasketItem.clear(session, user.id)