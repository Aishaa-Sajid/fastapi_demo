from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column                              

from src.database.config import Base       
from src.database.models.user import User  
from src.database.models.post import Post
from src.database.config import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(nullable=False)

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    # 🔹 Relationships
    posts: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )