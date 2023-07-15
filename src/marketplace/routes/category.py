from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User
from src.marketplace.models import Category
from src.auth.dependencies import get_current_user_authorizer
from src.marketplace.schemas.category import CategoryWithSubCategories
from src.marketplace.utils import category_to_schema

router = APIRouter(tags=["categories"])


@router.get("/categories",  tags=["categories"],
            response_model=list[CategoryWithSubCategories],
            status_code=status.HTTP_200_OK)
async def get_categories(page: Optional[int] = None, limit: Optional[int] = None,
                         user: User = Depends(get_current_user_authorizer(required=False)),
                         session: AsyncSession = Depends(get_async_session)):
    """ Вывод категорий с подкатегориями """
    skip = None
    if page and limit:
        skip = (page - 1) * limit

    res = await Category.get_many(session, limit, skip)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categories not found")

    list_categories = [category_to_schema(cat_model) for cat_model in res]

    return list_categories
