from sqladmin import ModelView

from src.auth.models import User
from src.marketplace.models import Product, Category, Subcategory, BasketItem


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_list = [ User.login, User.email, User.is_admin, User.basket, User.id,]

    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True


class ProductAdmin(ModelView, model=Product):
    name = "Продукт"
    name_plural = "Продукты"
    icon = "fa-solid fa-tag"

    column_list = [Product.name, Product.slug_name,
                   Product.price, Product.basket, Product.url_image_large,
                   Product.url_image_small, Product.url_image_medium, Product.id, ]
    form_excluded_columns = [Product.slug_name]


class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-list"

    column_list = [Category.name, Category.slug_name,
                   Category.subcategories, Category.url_image, Category.id, ]
    form_excluded_columns = [Category.slug_name]


class SubcategoryAdmin(ModelView, model=Subcategory):
    name = "Подкатегория"
    name_plural = "Подкатегории"
    icon = "fa-solid fa-table"

    column_list = [Subcategory.name, Subcategory.slug_name, Subcategory.category,
                   Subcategory.url_image, Subcategory.id, ]
    form_excluded_columns = [Subcategory.slug_name]


class BasketAdmin(ModelView, model=BasketItem):
    name = "Корзина"
    name_plural = "Корзины"
    icon = "fa-solid fa-basket-shopping"

    column_list = [BasketItem.user, BasketItem.product, BasketItem.count,
                   BasketItem.user_id, BasketItem.product_id, ]

