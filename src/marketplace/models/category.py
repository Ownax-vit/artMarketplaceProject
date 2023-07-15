from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


from src.models import Base, CategoryMixin
from src.models import CommonMixin


class Category(Base, CategoryMixin, CommonMixin):
    __tablename__ = "categories"

    subcategories: Mapped[list["Subcategory"] | None] = relationship(back_populates="category",
                                                                     cascade="all, delete-orphan",
                                                                     lazy='selectin')

