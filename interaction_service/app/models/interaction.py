from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Likes(SQLModel, table=True):
    __tablename__ = "likes"
    tweet_id: int = Field(primary_key=True)
    user_id: int = Field(primary_key=True)


class Comments(SQLModel, table=True):
    __tablename__ = "comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    tweet_id: int
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
