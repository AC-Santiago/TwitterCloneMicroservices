from pydantic import BaseModel


class RetweetBase(BaseModel):
    tweet_id: int


class RetweetCreate(RetweetBase):
    pass
