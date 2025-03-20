from pydantic import BaseModel


class LikeBase(BaseModel):
    tweet_id: int


class LikeCreate(LikeBase):
    pass
