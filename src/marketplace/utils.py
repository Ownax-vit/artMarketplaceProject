from src.marketplace.models import BasketItem
from src.marketplace.models.category import Category
from src.marketplace.schemas.basket import BaseBasketItem
from src.marketplace.schemas.category import CategoryWithSubCategories
from src.marketplace.schemas.subcategory import SubCategoryNested
from src.marketplace.schemas.product import ProductResponse
from src.marketplace.models.product import Product


def category_to_schema(category: Category) -> CategoryWithSubCategories:
    return CategoryWithSubCategories(
        id=category.id,
        slug_name=category.slug_name,
        name=category.name,
        url_image=category.url_image,
        subcategories=[SubCategoryNested(id=subcat.id,
                                         slug_name=subcat.slug_name,
                                         name=subcat.name,
                                         url_image=subcat.url_image
                                         ) for subcat in category.subcategories]
    )


def product_to_schema(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        slug_name=product.slug_name,
        name=product.name,
        category=product.subcategory.category.name,
        subcategory=product.subcategory.name,
        price=product.price,
        list_images=[product.url_image_small, product.url_image_medium, product.url_image_large],
    )


def basket_item_to_schema(basket: BasketItem) -> BaseBasketItem:
    return BaseBasketItem(
        id=basket.product.id,
        name=basket.product.name,
        price=basket.product.price,
        sum_price=basket.product.price * basket.count,
        count=basket.count
    )
