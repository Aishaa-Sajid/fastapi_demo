from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.post import Post
from src.database.models.vote import Vote


async def get_post(db: AsyncSession, post_id: int):
    """
    Check if a post exists.
    """
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_vote(db: AsyncSession, post_id: int, user_id: int):
    """
    Get existing vote for a user on a post.
    """
    stmt = select(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_vote(db: AsyncSession, post_id: int, user_id: int):
    """
    Create a new vote.
    """
    new_vote = Vote(post_id=post_id, user_id=user_id)
    db.add(new_vote)
    await db.commit()
    return new_vote


async def delete_vote(db: AsyncSession, post_id: int, user_id: int):
    """
    Delete a vote.
    """
    stmt = delete(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)

    await db.execute(stmt)
    await db.commit()
