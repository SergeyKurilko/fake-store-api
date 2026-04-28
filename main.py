from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse

from database.models import Base
from database.config import engine, AsyncSessionLocal
from database.mock_data import create_fake_products, check_products_exists
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

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import dotenv
    import uvicorn
    dotenv.load_dotenv()
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
