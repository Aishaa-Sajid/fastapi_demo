from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import SessionLocal


async def get_pg_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
