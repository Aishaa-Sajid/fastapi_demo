from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from .user import UserOut


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = {"from_attributes": True}


class PostOut(BaseModel):
    post: Post
    votes: int

    model_config = {"from_attributes": True}
