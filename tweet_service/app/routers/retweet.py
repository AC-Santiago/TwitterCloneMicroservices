from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.crud.retweet import (
    count_retweets_by_tweet,
    create_retweet,
    delete_retweet,
    get_retweet,
    get_retweets,
    get_retweets_by_tweet,
    get_retweets_by_user,
)
from app.crud.tweet import get_tweet
from app.database.connection import get_session
from app.schemas.retweet import RetweetCreate

router = APIRouter()


@router.get("/retweets/{tweet_id}", tags=["Retweets"])
def read_retweets_by_tweet(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    retweets = get_retweets_by_tweet(session, tweet_id)
    if not retweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retweets not found",
        )
    return retweets


@router.get("/retweets/", tags=["Retweets"])
def read_retweets(session: Session = Depends(get_session)):
    retweets = get_retweets(session)
    if not retweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retweets not found",
        )
    return retweets


@router.get("/retweets/user/{user_id}", tags=["Retweets"])
def read_retweets_by_user(
    user_id: int, session: Annotated[Session, Depends(get_session)]
):
    retweets = get_retweets_by_user(session, user_id)
    if not retweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retweets not found",
        )
    return retweets


@router.get("/retweet/{user_id}/{tweet_id}", tags=["Retweets"])
def read_retweet(
    user_id: int,
    tweet_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    retweet = get_retweet(session, user_id, tweet_id)
    if not retweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retweet not found",
        )
    return retweet


@router.get("/retweets/count/tweet/{tweet_id}")
def get_count_retweets_by_tweet(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    count_retweets = count_retweets_by_tweet(session, tweet_id)
    return JSONResponse(
        content={"total_retweets": count_retweets},
        status_code=status.HTTP_200_OK,
    )


@router.post("/retweet/", tags=["Retweets"])
def create_retweet_end_point(
    retweet: RetweetCreate, session: Annotated[Session, Depends(get_session)]
):
    tweet = get_tweet(session, retweet.tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found",
        )
    retweet_query = get_retweet(session, retweet.user_id, retweet.tweet_id)
    if retweet_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't retweet the same tweet twice",
        )
    try:
        db_retweet = create_retweet(session, retweet)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {e}",
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=db_retweet,
    )


@router.delete("/retweet/{user_id}/{tweet_id}", tags=["Retweets"])
def delete_retweet_endpoint(
    user_id: int,
    tweet_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    retweet = get_retweet(session, user_id, tweet_id)
    if not retweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retweet not found",
        )
    status_deleted = delete_retweet(session, user_id, tweet_id)
    if not status_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting retweet",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
