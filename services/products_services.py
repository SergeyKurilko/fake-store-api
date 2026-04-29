from sqlalchemy.ext.asyncio import AsyncSession
from repository import products_repo as pr
from database.models import Product

async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    """Получение продукта по product_id"""
    return await pr.get_product_by_id(session, product_id)

async def get_products_by_category_and_page(
        session: AsyncSession,
        category_id: int,
        page: int,
        limit: int,
):
    """Получения списка продуктов по category_id и page (offset = page * 20)"""
    return await pr.get_products_by_category_and_page(session, category_id, page, limit)