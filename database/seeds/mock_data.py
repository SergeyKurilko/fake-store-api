import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from settings import BASE_DIR
from database.models import Product, ProductCategory

mock_categories = [
    {"id": 1, "title": "electronics"},
    {"id": 2, "title": "jewelery"},
    {"id": 3, "title": "men's clothing"},
    {"id": 4, "title": "women's clothing"},
    {"id": 5, "title": "sports"},
    {"id": 6, "title": "books"},
    {"id": 7, "title": "toys"},
    {"id": 8, "title": "home"},
]


async def check_products_exists(session: AsyncSession) -> bool:
    """Асинхронная проверка наличия продуктов"""
    stmt = select(Product)
    result = await session.execute(stmt)
    return result.scalars().first() is not None


async def create_fake_products(session: AsyncSession):
    """Асинхронное создание тестовых продуктов и категорий"""
    for mock_category in mock_categories:
        new_category = ProductCategory(**mock_category)
        session.add(new_category)

    await session.commit()

    with open(f"{BASE_DIR}/mock_products.json") as file:
        mock_products = json.loads(file.read())
    for mock_product in mock_products:
        new_product = Product(**mock_product)
        session.add(new_product)

    await session.commit()
