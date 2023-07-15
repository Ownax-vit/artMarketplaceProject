import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import insert

from tests.conftest import fake

from src.marketplace.models import Category, Subcategory
from tests.conftest import async_session_maker


@pytest.fixture(scope="function")
def test_category() -> dict:
    category_data = {
        "name": fake.text(10),
        "slug_name": fake.text(30),
        "url_image": fake.image_url()
    }
    return category_data


async def test_get_category(client: TestClient, test_category: dict):
    async with async_session_maker() as session:
        stmt = insert(Category).values(
                                       name=test_category["name"],
                                       slug_name=test_category["slug_name"],
                                       url_image=test_category["url_image"])
        await session.execute(stmt)
        await session.commit()

    resp = client.get("/api_v1/categories")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) != 0
    # TODO дописать тесты, на пагинацию


