from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/" \
               f"{settings.db_name}"

# create async engine for interaction with database
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

# create session for the interaction with database
async_session_maker = sessionmaker(engine, class_=AsyncSession,
                                   expire_on_commit=False,
                                   autocommit=False,
                                   autoflush=False,)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
