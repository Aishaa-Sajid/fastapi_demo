from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.dependency import get_pg_db
from src.crud import user_crud

router = APIRouter(tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_pg_db)):
    """
    API endpoint to create a new user.
    """

    return await user_crud.create_user(db, user)


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_pg_db)):
    """
    API endpoint to get a user by ID.
    """
    user = await user_crud.get_user_by_id(db, id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    return user
