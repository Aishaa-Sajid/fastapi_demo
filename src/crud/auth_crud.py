from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import models


async def get_user_by_id(db: AsyncSession, user_id: int):
    """
    Fetch user by ID from database.

    Args:
        db (AsyncSession): database session
        user_id (int): user id

    Returns:
        models.User | None
    """
    result = await db.execute(select(models.User).where(models.User.id == user_id))

    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    """
    Fetch user by email from database.

    Args:
        db (AsyncSession): database session
        email (str): user email

    Returns:
        models.User | None
    """
    result = await db.execute(select(models.User).where(models.User.email == email))

    return result.scalars().first()
