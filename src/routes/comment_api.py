from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database.dependency import get_pg_db
from src.crud import comment_crud
from src.database.models import Comment
from sqlalchemy import select
from src.core.security import get_current_user
from src.schemas.comment import CommentOut, CommentCreate, CommentUpdate

router = APIRouter(tags=["Comments"])


@router.get("/post/{post_id}", response_model=list[CommentOut])
async def get_comments_for_post(
    post_id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    """
    Get all comments for a specific post with pagination.
    """
    return await comment_crud.get_comments_by_post(db, post_id, limit, skip)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentOut)
async def create_comment(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new comment.
    """
    return await comment_crud.create_comment(db, comment, current_user.id)


@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Get single comment by ID.
    """
    comment = await comment_crud.get_comment_by_id(db, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"comment with id {comment_id} not found",
        )

    return comment


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    updated_comment: CommentUpdate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Update comment (owner only).
    """
    stmt = (
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.id == comment_id)
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to update this comment"
        )

    updated_data = updated_comment.model_dump(exclude_unset=True)
    updated = await comment_crud.update_comment(db, comment_id, updated_data)

    return updated


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Delete comment (owner only).
    """
    stmt = (
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.id == comment_id)
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to delete this comment"
        )

    return await comment_crud.delete_comment(db, comment_id)


@router.get("/user/{user_id}", response_model=list[CommentOut])
async def get_comments_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    """
    Get all comments by a specific user with pagination.
    """
    return await comment_crud.get_comments_by_user(db, user_id, limit, skip)
