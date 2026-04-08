from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.database.config import Base


class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

    user = relationship("User", back_populates="votes")
    posts = relationship("Post", back_populates="votes")
