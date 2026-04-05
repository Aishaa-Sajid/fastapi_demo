from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.dependency import get_pg_db
from src.crud import vote_crud
from src.core import security

router = APIRouter(tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote,
    db: AsyncSession = Depends(get_pg_db),
    current_user=Depends(security.get_current_user),
):
    """
    Toggle vote on a post:
    - dir = 1 → add vote
    - dir = 0 → remove vote
    """

    post = await vote_crud.get_post(db, vote.post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist",
        )

    found_vote = await vote_crud.get_vote(db, vote.post_id, current_user.id)

    # =========================
    # ADD VOTE
    # =========================
    if vote.dir == 1:

        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post",
            )

        await vote_crud.create_vote(db, vote.post_id, current_user.id)

        return {"message": "vote added successfully"}

    # =========================
    # DELETE VOTE
    # =========================
    else:

        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )

        await vote_crud.delete_vote(db, vote.post_id, current_user.id)

        return {"message": "vote removed successfully"}
