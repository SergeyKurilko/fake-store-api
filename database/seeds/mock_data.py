import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from settings import BASE_DIR
from database.models import Product, ProductCategory

mock_categories = [
    {"id": 1, "title": "Электроника"},
    {"id": 2, "title": "Украшения"},
    {"id": 3, "title": "Мужская одежда"},
    {"id": 4, "title": "Женская одежда"},
    {"id": 5, "title": "Спорт"},
    {"id": 6, "title": "Книги"},
    {"id": 7, "title": "Игры"},
    {"id": 8, "title": "Для дома"},
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
