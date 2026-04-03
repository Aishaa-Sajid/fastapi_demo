from pydantic import BaseModel, Field

# from pydantic.types import conint
from typing import Annotated


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]
