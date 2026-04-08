from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.schemas.post import PostCreate
from src.database.models.vote import Vote
from src.database.models.post import Post


async def get_posts(db: AsyncSession, limit: int, skip: int, search: str | None = None):
    """
    Fetch all posts with vote count, pagination, and search filter.
    Async SQLAlchemy 2.0 version.
    """
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .options(selectinload(Post.owner))
        .group_by(Post.id)
        .limit(limit)
        .offset(skip)
    )

    if search:
        stmt = stmt.where(Post.title.contains(search))

    result = await db.execute(stmt)

    posts = []
    for post, votes in result.all():
        posts.append({"post": post, "votes": votes})

    return posts


async def create_post(db: AsyncSession, post: PostCreate, user_id: int) -> Post:
    """
    Create a new post (async).
    """
    new_post = Post(owner_id=user_id, **post.model_dump())

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_post(db: AsyncSession, post_id: int):
    """
    Fetch single post with vote count.
    """
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .options(selectinload(Post.owner))
        .group_by(Post.id)
        .where(Post.id == post_id)
    )

    result = await db.execute(stmt)
    row = result.first()

    if not row:
        return None

    post, votes = row

    return {"Post": post, "votes": votes}


async def delete_post(db: AsyncSession, post: Post):
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
    stmt = select(Post).options(selectinload(Post.owner)).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        return None

    for key, value in updated_data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)

    return post
