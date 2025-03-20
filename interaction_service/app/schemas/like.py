from pydantic import BaseModel


class LikeBase(BaseModel):
    user_id: int
    tweet_id: int


class LikeCreate(LikeBase):
    pass
