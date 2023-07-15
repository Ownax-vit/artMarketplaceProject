from decimal import Decimal

from pydantic import Field, AnyUrl

from src.marketplace.schemas.base import BaseNaming, Base


class Product(Base, BaseNaming):
    url_image_small: AnyUrl = Field(..., max_length=255)
    url_image_medium: AnyUrl = Field(..., max_length=255)
    url_image_large: AnyUrl = Field(...,  max_length=255)
    price: Decimal = Field(...)


class ProductResponse(Base, BaseNaming):
    category: str
    subcategory: str
    price: Decimal = Field(...)
    list_images: list[AnyUrl] = Field(min_length=3, max_length=3)