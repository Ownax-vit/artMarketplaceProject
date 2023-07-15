
from fastapi import FastAPI
from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src.config import settings
from src.auth.router import router as auth_router
from src.marketplace.routes.category import router as router_category
from src.marketplace.routes.product import router as router_product
from src.marketplace.routes.basket import router as router_basket
from src.database import engine
from src.admin.router import UserAdmin, ProductAdmin, CategoryAdmin, \
    SubcategoryAdmin, BasketAdmin
from src.admin.auth import AdminAuth


router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(router_category, prefix="/api_v1")
router.include_router(router_product, prefix="/api_v1")
router.include_router(router_basket, prefix="/api_v1")

app = FastAPI(title=settings.app_name)

authentication_backend = AdminAuth(secret_key=settings.secret_key.get_secret_value())
admin = Admin(app, engine, authentication_backend=authentication_backend)

app.include_router(router)
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(SubcategoryAdmin)
admin.add_view(BasketAdmin)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)