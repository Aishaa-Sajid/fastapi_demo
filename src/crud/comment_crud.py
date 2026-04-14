from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from collections.abc import Sequence
from src.schemas.comment import CommentCreate, CommentUpdate
from src.database.models.comment import Comment


async def create_comment(
    db: AsyncSession, comment: CommentCreate, user_id: int
) -> Comment:
    """
    Create a new comment in the database.

    Args:
        db (AsyncSession): database session
        comment (CommentCreate): comment input schema
        user_id (int): ID of the user creating the comment

    Returns:
        models.Comment: created comment instance
    """
    new_comment = Comment(
        content=comment.content, post_id=comment.post_id, user_id=user_id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment


async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    """
    Fetch a comment by ID.

    Args:
        db (AsyncSession): database session
        comment_id (int): comment ID

    Returns:
        models.Comment | None
    """
    stmt = (
        select(Comment)
        .options(selectinload(Comment.user), selectinload(Comment.post))
        .where(Comment.id == comment_id)
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_comments_by_post(
    db: AsyncSession, post_id: int, limit: int = 10, skip: int = 0
) -> Sequence[Comment]:
    """
    Fetch comments for a specific post with pagination.

    Args:
        db (AsyncSession): database session
        post_id (int): post ID
        limit (int): maximum number of comments to return
        skip (int): number of comments to skip

    Returns:
        sequence[models.Comment]
    """
    stmt = (
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.post_id == post_id)
        .limit(limit)
        .offset(skip)
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_comments_by_user(
    db: AsyncSession, user_id: int, limit: int = 10, skip: int = 0
) -> Sequence[Comment]:
    """
    Fetch comments by a specific user with pagination.

    Args:
        db (AsyncSession): database session
        user_id (int): user ID
        limit (int): maximum number of comments to return
        skip (int): number of comments to skip

    Returns:
        sequence[models.Comment]
    """
    stmt = (
        select(Comment)
        .options(selectinload(Comment.post))
        .where(Comment.user_id == user_id)
        .limit(limit)
        .offset(skip)
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def update_comment(
    db: AsyncSession, comment_id: int, updated_data: CommentUpdate, user_id: int
) -> Comment | None:
    """
    Update a comment.

    Args:
        db (AsyncSession): database session
        comment_id (int): comment ID
        updated_data (dict): fields to update

    Returns:
        models.Comment | None
    """
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if not comment:
        return None

    update_dict = updated_data.model_dump(
        exclude_unset=True
    )  # exclude_unset=True already removes missing fields

    # schema--> dict conversion
    for key, value in update_dict.items():
        # if value is None:
        #     continue
        if hasattr(comment, key):
            setattr(comment, key, value)

    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(db: AsyncSession, comment_id: int) -> dict:
    """
    Delete a comment.

    Args:
        db (AsyncSession): database session
        comment_id (int): comment ID

    Returns:
        dict: success message
    """
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if not comment:
        return {"message": "Comment not found"}

    await db.delete(comment)
    await db.commit()

    return {"message": "Comment deleted successfully"}
