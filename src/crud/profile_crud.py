from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.profile import Profile


async def get_profile_by_user_id(db: AsyncSession, user_id: int):
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_profile(db: AsyncSession, user_id: int, data: dict):
    profile = Profile(user_id=user_id, **data)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile(db: AsyncSession, profile, data: dict):
    for key, value in data.items():
        if value is not None:
            setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile


# Note: Deleting a profile will also delete the associated user due to the cascade delete relationship defined in the models
async def delete_profile(db: AsyncSession, profile):
    await db.delete(profile)
    await db.commit()
