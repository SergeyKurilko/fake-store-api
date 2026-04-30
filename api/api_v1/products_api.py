from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_db
from database.models import Product
from schemas import ProductSchema, ProductListByCategory
from services import products_services as ps
from settings import BEARER_TOKEN

from schemas import ProductsByCategoryRequest


security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Асинхронная проверка токена"""
    token = credentials.credentials
    if token != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    return token

router = APIRouter(dependencies=[Depends(verify_token)], tags=["products"])


@router.get("/products/{product_id}")
async def get_product_by_id(
        product_id: int,
        session: AsyncSession = Depends(get_db)
) -> ProductSchema:
    """Получение одного продукта по id продукта"""
    product: Product | None = await ps.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductSchema.model_validate(product)

@router.get("/products")
async def get_products_by_category(
        request: ProductsByCategoryRequest = Depends(),
        session: AsyncSession = Depends(get_db)
) -> ProductListByCategory | None:
    """Получение списка продуктов по category_id и page."""
    items = await ps.get_products_by_category_and_page(
        session=session,
        category_id=request.category_id,
        page=request.page,
        limit=request.limit
    )
    if not items:
        raise HTTPException(status_code=404, detail="Products not found")
    return ProductListByCategory(
        items=items[:-1] if len(items) > 1 else items,
        has_more=bool(len(items) > request.limit), # нашлось продуктов больше, чем запрашивали в limit
    )