from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import ForeignKey, Integer, Select, Delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from starlette import status

from src.models import Base


class BasketItem(Base):
    """ Model basket of products """

    __tablename__ = "baskets"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="basket", lazy="joined", join_depth=1)
    user: Mapped["User"] = relationship(back_populates="basket", lazy="joined", join_depth=1)

    def __repr__(self):
        return f"Count: {self.count}"

    @classmethod
    async def get_all_products(cls, session: AsyncSession, user_id: UUID):
        from src.auth.models import User
        from src.marketplace.models import Product

        stmt = Select(cls).join(User).join(Product).where(User.id == user_id)

        rows = await session.execute(stmt)
        res = rows.scalars().unique().all()
        return res

    @classmethod
    async def find(cls, session: AsyncSession, product_id: UUID, user_id: UUID):
        stmt = Select(cls).where(cls.user_id == user_id).where(cls.product_id == product_id)
        result = await session.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Current product not found in basket for user")
        return instance

    @classmethod
    async def clear(cls, session: AsyncSession, user_id: UUID):
        stmt = Delete(cls).where(cls.user_id == user_id)
        try:
            await session.execute(stmt)
            await session.commit()
            return True
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Error while clear basket")

