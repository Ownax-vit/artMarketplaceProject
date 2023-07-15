from typing import Optional
from uuid import UUID, uuid4

from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from pydantic import ConfigDict
from sqlalchemy import String, CheckConstraint, Select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import validates


@as_declarative()
class Base:

    async def save(self, session: AsyncSession):
        try:
            session.add(self)
            return await session.commit()
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=repr(exc)) from exc

    async def delete(self, session: AsyncSession):
        try:
            await session.delete(self)
            await session.commit()
            return True
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=repr(exc)) from exc

    async def update(self, session: AsyncSession, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            return await session.commit()
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=repr(exc)) from exc

    async def save_or_update(self, session: AsyncSession):
        try:
            session.add(self)
            return await session.commit()
        except IntegrityError as exc:
            if isinstance(exc.orig, UniqueViolationError):
                return await session.merge(self)
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail=repr(exc)) from exc
        finally:
            await session.close()

    @classmethod
    async def get_many(cls, session: AsyncSession, limit: Optional[int] = None, offset: Optional[int] = None):
        stmt = Select(cls)
        if limit and offset:
            stmt = stmt.limit(limit).offset(offset)

        rows = await session.execute(stmt)
        res = rows.scalars().unique().all()
        return res


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""
    model_config = ConfigDict(from_attributes=True)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    def __repr__(self):
        return f"{self.id}"


class NamingMixin:
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"

    __table_args__ = (
        CheckConstraint('char_length(name) > 4',
                        name='name_min_length'),
        CheckConstraint('char_length(slug_name) > 4',
                        name='slug_name_min_length'),
    )

    @validates("name", "slug_name")
    def validate_name(self, key, name):
        if len(name) <= 4:
            raise ValueError('Name too short')
        return name


class CategoryMixin(NamingMixin):
    url_image: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
