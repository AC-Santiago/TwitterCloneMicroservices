from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.crud.tweet import create_tweet, get_tweet, get_tweets
from app.database.connection import get_session
from app.schemas.tweet import TweetBase, TweetCreate, TweetOut

router = APIRouter()


@router.get("/tweets/{tweet_id}", tags=["Tweets"], response_model=TweetOut)
def read_tweet(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    tweet = get_tweet(session, tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return tweet


@router.get("/tweets/", tags=["Tweets"], response_model=List[TweetOut])
def read_tweets(session: Session = Depends(get_session)):
    tweets = get_tweets(session)
    return tweets


@router.post("/tweet/", tags=["Tweets"])
def create_tweets(
    session: Annotated[Session, Depends(get_session)],
    new_tweet: TweetBase,
    user_id: int,
):
    tweet = TweetCreate(user_id=user_id, content=new_tweet.content)
    create_tweet(session, tweet)
    return JSONResponse(
        {"message": "Tweet successfully created"},
        status_code=status.HTTP_201_CREATED,
    )
