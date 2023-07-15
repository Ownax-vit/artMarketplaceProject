from typing import Optional

from pydantic import Field

from src.marketplace.schemas.base import BaseNaming, BaseCategory, Base
from src.marketplace.schemas.subcategory import SubCategoryNested


class Category(Base, BaseCategory, BaseNaming):
    pass


class CategoryWithSubCategories(Category):
    subcategories: Optional[list[SubCategoryNested]] = []

