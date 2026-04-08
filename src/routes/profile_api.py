from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.dependency import get_pg_db
from src.core.security import get_current_user
from src.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate
from src.crud import profile_crud

router = APIRouter(tags=["Profile"])


# Create Profile (only one allowed)
@router.post("/", response_model=ProfileOut)
async def create_profile(
    profile: ProfileCreate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    existing = await profile_crud.get_profile_by_user_id(db, current_user.id)

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    return await profile_crud.create_profile(db, current_user.id, profile.model_dump())


#  Get My Profile
@router.get("/", response_model=ProfileOut)
async def get_my_profile(
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    profile = await profile_crud.get_profile_by_user_id(db, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


# Update Profile (partial update supported)
@router.put("/", response_model=ProfileOut)
async def update_profile(
    updated_data: ProfileUpdate,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    profile = await profile_crud.get_profile_by_user_id(db, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return await profile_crud.update_profile(db, profile, updated_data.model_dump())


# Delete Profile
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_profile(
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(get_current_user),
):
    profile = await profile_crud.get_profile_by_user_id(db, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    await profile_crud.delete_profile(db, profile)

    return {"message": "Profile deleted successfully"}
