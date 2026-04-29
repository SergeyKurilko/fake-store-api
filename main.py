import glob

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from database.models import Base
from database.config import engine, AsyncSessionLocal
from database.seeds.mock_data import create_fake_products, check_products_exists
from api import products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup: создаем таблицы и наполняем данными
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Проверяем и наполняем БД
    async with AsyncSessionLocal() as session:
        if not await check_products_exists(session):
            await create_fake_products(session)

    yield

    # Shutdown: закрываем соединения
    await engine.dispose()


# Создаем приложение с lifespan
app = FastAPI(lifespan=lifespan)
app.include_router(products_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_frontend():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/img/{product_article}", include_in_schema=False)
async def serve_static(product_article: str):
    file_path = "static/img/def_img.png"
    try:
        split_article = product_article.split("-")
        category = split_article[-1]
        category = category.split(".")[0]

        # Ищем файл, начинающийся с category-
        pattern = f"static/img/{category}-*"
        matching_files = glob.glob(pattern)
        if matching_files:
            file_path = matching_files[0]
    finally:
        return FileResponse(
            path=file_path,
            media_type="image/png",
            headers={"Content-Disposition": "inline"}  # Открыть в браузере
        )

@app.get("/random-product-card", response_class=HTMLResponse, include_in_schema=False)
async def random_product_card_html():
    with open("templates/products_cards/random_product_card.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
