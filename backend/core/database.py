from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.core.config import settings
from backend.models.database import Base
import asyncio

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
