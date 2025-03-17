from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Tweets(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    content: str

    retweets: list["Retweets"] = Relationship(back_populates="tweet")


class Retweets(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    tweet_id: int = Field(foreign_key="tweets.id", primary_key=True)

    tweet: Tweets = Relationship(back_populates="retweets")
