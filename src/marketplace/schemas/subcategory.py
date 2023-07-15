from typing import Optional

from src.marketplace.models import Subcategory
from src.marketplace.schemas.base import BaseNaming, Base, BaseCategory
from src.marketplace.schemas.product import Product


class SubCategoryNested(BaseNaming, Base, BaseCategory):
    pass

    class Meta:
        orm_model = Subcategory

    class Config:
        from_attributes = True


class SubCategoryWithProducts(Base, BaseNaming):
    products: Optional[list[Product]]

