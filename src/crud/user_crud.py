from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import utils
from src.schemas.user import UserCreate
from src.database.models.user import User


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (AsyncSession): database session
        user (UserCreate): user input schema

    Returns:
        models.User: created user instance
    """
    hashed_password = utils.hash(user.password)

    new_user = User(
        **user.model_dump(exclude={"password"}), password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Fetch a user by ID.

    Args:
        db (AsyncSession): database session
        user_id (int): user id

    Returns:
        models.User | None
    """

    result = await db.execute(select(User).where(User.id == user_id))

    return result.scalar_one_or_none()
