from pydantic import BaseModel
from datetime import datetime
from .user import UserOut


class CommentBase(BaseModel):
    content: str
    post_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str | None = None


class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserOut

    model_config = {"from_attributes": True}
