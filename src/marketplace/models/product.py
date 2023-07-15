from typing import Optional
from uuid import UUID
from decimal import Decimal

from sqlalchemy import ForeignKey, Select
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from src.models import Base
from src.models import CommonMixin, NamingMixin


class Product(Base, NamingMixin, CommonMixin):
    __tablename__ = "products"

    subcategory_id: Mapped[UUID] = mapped_column(ForeignKey("subcategories.id", ondelete="CASCADE"))
    url_image_small: Mapped[str] = mapped_column(String(255), nullable=False)
    url_image_medium: Mapped[str] = mapped_column(String(255), nullable=False)
    url_image_large: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    subcategory: Mapped['Subcategory'] = relationship(back_populates="products", lazy='joined', join_depth=1)
    basket: Mapped[list['BasketItem'] | None] = relationship(back_populates="product",
                                                             cascade="all, delete-orphan")
