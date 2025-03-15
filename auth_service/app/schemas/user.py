from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    full_name: str
    biography: str | None = None
    password: str = "*****"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    biography: Optional[str] = None
