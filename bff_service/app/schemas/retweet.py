from pydantic import BaseModel


class RetweetCreate(BaseModel):
    tweet_id: int
