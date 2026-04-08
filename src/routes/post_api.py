from fastapi import APIRouter, Depends, status, HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload
from src import schemas
from src.database.dependency import get_pg_db
from src.crud import post_crud
from src.database import models
from sqlalchemy import select
from src.core.security import get_current_user

router = APIRouter(tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str | None = Query(default=None)):
    """
    Get all posts with pagination and search.
    """
    return await post_crud.get_posts(db, limit, skip, search)

@router.get("/no_auth", response_model=List[schemas.PostOut])
async def get_posts_no_auth(
    db: AsyncSession = Depends(get_pg_db),
    limit: int = 10,
    skip: int = 0,
    search: str | None = Query(default=None)):
    """
    Get all posts with pagination and search.
    """
    return await post_crud.get_posts(db, limit, skip, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new post.
    """
    return await post_crud.create_post(db, post, current_user.id)


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(
    id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Get single post by ID.
    """
    post = await post_crud.get_post(db, id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_post(
    id: int,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Delete post (owner only).
    """
    # stmt = select(models.Post).where(models.Post.id == id)
    stmt = (
        select(models.Post)
        .options(selectinload(models.Post.owner))
        .where(models.Post.id == id)
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

    return await post_crud.delete_post(db, post)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    """
    Update post (owner only).
    """
    # stmt = select(models.Post).where(models.Post.id == id)
    stmt = (
        select(models.Post)
        .options(selectinload(models.Post.owner))
        .where(models.Post.id == id)
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this post")

    updated = await post_crud.update_post(db, id, updated_post.model_dump())

    return updated
