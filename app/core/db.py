from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.config import settings
import asyncio

# Fix connection string for asyncpg
DB_URL = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DB_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    """Dependency to get async SQL session"""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Global session for tools
async def get_global_session():
    async with SessionLocal() as session:
        return session