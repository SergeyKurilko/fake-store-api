from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Для SQLite используем aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///fakestore.db"
# Для PostgreSQL:
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Создаем асинхронный engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Логирование SQL запросов
    future=True,
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для FastAPI"""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

@asynccontextmanager
async def get_db_context():
    """Асинхронный контекстный менеджер для скриптов"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()