from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from src.models import Base, CategoryMixin
from src.models import CommonMixin


class Subcategory(Base, CategoryMixin, CommonMixin):
    __tablename__ = "subcategories"

    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))

    category: Mapped["Category"] = relationship(back_populates="subcategories", lazy="joined")
    products: Mapped[list["Product"] | None] = relationship(back_populates="subcategory",
                                                            cascade="all, delete-orphan")