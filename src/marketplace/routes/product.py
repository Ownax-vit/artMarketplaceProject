from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User
from src.marketplace.models import Product
from src.auth.dependencies import get_current_user_authorizer
from src.marketplace.schemas.product import ProductResponse
from src.marketplace.utils import product_to_schema

router = APIRouter(tags=["categories"])


@router.get("/products",  tags=["categories"],
            response_model=list[ProductResponse],
            status_code=status.HTTP_200_OK)
async def get_products(page: Optional[int] = None, limit: Optional[int] = None,
                         user: User = Depends(get_current_user_authorizer(required=False)),
                         session: AsyncSession = Depends(get_async_session)):
    """ Вывод продуктов """
    skip = None
    if page and limit:
        skip = (page - 1) * limit

    res = await Product.get_many(session, limit, skip)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Products not found")

    list_products = [product_to_schema(product) for product in res]

    return list_products
