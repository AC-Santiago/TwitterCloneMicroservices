from pydantic import BaseModel


class RetweetCreate(BaseModel):
    user_id: int
    tweet_id: int


class RetweetBase(BaseModel):
    tweet_id: int


class RetweetOut(RetweetBase):
    id: int
    user_name: str
