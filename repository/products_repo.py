from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product, ProductCategory


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    """Асинхронное получение продукта по ID"""
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_products_by_category_and_page(
    session: AsyncSession, category_id: int, page: int, limit: int
):
    """Получения списка продуктов по category_id и page (offset = page * 20)"""
    stmt = (
        select(
            Product.id,
            Product.title,
            Product.price,
            Product.description,
            Product.category_id,
            Product.image,
            Product.rating,
            ProductCategory.title.label("category_name")
        )
        .join(ProductCategory, Product.category_id == ProductCategory.id)
        .where(Product.category_id == category_id))

    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit + 1)
    result = await session.execute(stmt)
    return result.all()
