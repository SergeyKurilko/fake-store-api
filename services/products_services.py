from sqlalchemy.ext.asyncio import AsyncSession
from repository import products_repo as pr
from database.models import Product

async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    """Асинхронное получение продукта"""
    return await pr.get_product_by_id(session, product_id)