from pydantic import BaseModel


class TweetBase(BaseModel):
    content: str
