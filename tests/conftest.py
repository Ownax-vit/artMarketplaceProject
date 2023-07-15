import asyncio
from typing import AsyncGenerator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database import get_async_session
from src.config import settings
from src.main import app
from src.models import Base

DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.test_db_user}:" \
                    f"{settings.test_db_pass}@" \
                    f"{settings.test_db_host}:" \
                    f"{settings.test_db_port}/" \
                    f"{settings.test_db_name}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
fake = Faker(["en_Us", "ru_RU"])


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def init_delete_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


client = TestClient(app)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncGenerator, None]:
    with TestClient(app=app, base_url="http://test", headers={}) as client:
        yield client

