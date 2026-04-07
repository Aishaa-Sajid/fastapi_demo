from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src import schemas
from src.database import models


async def get_posts(db: AsyncSession, limit: int, skip: int, search: str | None = None):
    """
    Fetch all posts with vote count, pagination, and search filter.
    Async SQLAlchemy 2.0 version.
    """
    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .options(selectinload(models.Post.owner))
        .group_by(models.Post.id)
        # .where(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    )

    if search:
        stmt = stmt.where(models.Post.title.contains(search))

    result = await db.execute(stmt)
    # return result.all()

    posts = []
    for post, votes in result.all():
        posts.append({
            "post": post,
            "votes": votes
        })

    return posts

async def create_post(db: AsyncSession, post: schemas.PostCreate, user_id: int) -> Post:
    """
    Create a new post (async).
    """
    new_post = models.Post(owner_id=user_id, **post.model_dump())

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_post(db: AsyncSession, post_id: int):
    """
    Fetch single post with vote count.
    """
    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .options(selectinload(models.Post.owner))
        .group_by(models.Post.id)
        .where(models.Post.id == post_id)
    )

    result = await db.execute(stmt)
    # return result.first()
    row = result.first()

    if not row:
        return None

    post, votes = row
    # post.votes = votes   # attach votes

    # return post
    return {
    "Post": post,
    "votes": votes
}


async def delete_post(db: AsyncSession, post: models.Post):
    """
    Delete a post instance.
    """
    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully"}

async def update_post(db: AsyncSession, post_id: int, updated_data: dict):
    """
    Update post using async SQLAlchemy 2.0 style.
    """
    stmt = (
    select(models.Post)
    .options(selectinload(models.Post.owner))   # 🔥 add this
    .where(models.Post.id == post_id))
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        return None

    for key, value in updated_data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)

    return post
