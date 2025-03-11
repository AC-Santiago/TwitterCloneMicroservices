from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    password: str = Field(default=None)
    full_name: str = Field(default=None)
    biography: str = Field(default="")

    # Relación con Tweet
    # tweets: List["Tweets"] = Relationship(back_populates="user")

    profile_photo: Optional["ProfilePhotos"] = Relationship(
        back_populates="user"
    )


class ProfilePhotos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str
    file_name: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    user_id: int = Field(foreign_key="users.id", unique=True)

    user: Optional[Users] = Relationship(back_populates="profile_photo")
