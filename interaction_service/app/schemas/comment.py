from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    user_id: int


class CommentCreate(CommentBase):
    tweet_id: int
