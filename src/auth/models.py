from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Boolean, Select
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base
from src.models import CommonMixin
from src.marketplace.models import BasketItem


class User(Base, CommonMixin):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean,  nullable=False, default=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    salt: Mapped[str] = mapped_column(String(255), nullable=False)

    basket: Mapped[list["BasketItem"] | None] = relationship(back_populates="user",
                                                             cascade="all, delete")

    def __repr__(self):
        return f"{self.email} {self.login}"

    @classmethod
    async def check_login(cls, login: str, session: AsyncSession):
        stmt = select(cls).where(cls.login == login)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user:
            return user

    @classmethod
    async def check_email(cls, email: str, session: AsyncSession):
        stmt = select(cls).where(cls.email == email)
        res = await session.execute(stmt)
        user = res.scalars().first()
        if user:
            return user

