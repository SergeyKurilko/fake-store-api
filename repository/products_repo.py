from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product

async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    """Асинхронное получение продукта по ID"""
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()