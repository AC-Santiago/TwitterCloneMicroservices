from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.crud.tweet import (
    create_tweet,
    get_tweet,
    get_tweets,
    get_tweets_by_user,
    get_tweets_retweeted_by_user,
)
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


@router.get(
    "/tweets/user/{user_id}", tags=["Tweets"], response_model=List[TweetOut]
)
def read_tweets_by_user(user_id: int, session: Session = Depends(get_session)):
    tweets = get_tweets_by_user(session, user_id)
    if not tweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweets not found"
        )
    return tweets


@router.get("/tweets/retweeted/{user_id}", tags=["Tweets"])
def read_tweets_retweeted_by_user(
    user_id: int, session: Annotated[Session, Depends(get_session)]
):
    tweets = get_tweets_retweeted_by_user(session, user_id)
    return tweets


@router.post("/tweet/", tags=["Tweets"])
def create_tweets(
    session: Annotated[Session, Depends(get_session)],
    new_tweet: TweetBase,
    user_id: int,
):
    tweet = TweetCreate(user_id=user_id, content=new_tweet.content)
    new_tweet_create = create_tweet(session, tweet)
    return JSONResponse(
        content=new_tweet_create,
        status_code=status.HTTP_201_CREATED,
    )
