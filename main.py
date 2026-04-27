import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from contextlib import asynccontextmanager

from database.models import Base
from database.config import engine, AsyncSessionLocal
from database.mock_data import create_fake_products, check_products_exists
from api import products_router

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Асинхронная проверка токена"""
    token = credentials.credentials
    if token != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    return token


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
app = FastAPI(dependencies=[Depends(verify_token)], lifespan=lifespan)
app.include_router(products_router)

if __name__ == "__main__":
    import dotenv
    import uvicorn
    dotenv.load_dotenv()
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
