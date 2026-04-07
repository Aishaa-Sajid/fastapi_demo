from pydantic import BaseModel

class ProfileBase(BaseModel):
    name: str
    address: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True