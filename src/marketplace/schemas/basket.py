from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class BaseBasketItem(BaseModel):
    """ конкретный тип продукта в корзине """
    id: UUID = Field(...)
    name: str = Field(...)
    price: Decimal = Field(...)
    sum_price: Decimal = Field(...) # сумма за один тип продуктов
    count: int = Field(...)


class UpdateBasketItem(BaseModel):
    count: int = Field(...)


class CreateBasketItem(UpdateBasketItem):
    product_id: UUID = Field(...)


class ResponseBasketItem(CreateBasketItem):
    user_id: UUID = Field(...)

    class Config:
        from_attributes = True


class Basket(BaseModel):
    """ вся корзина """
    sum: Decimal = Field(...)
    count: int = Field(...)
    list_products: list[BaseBasketItem] = []
