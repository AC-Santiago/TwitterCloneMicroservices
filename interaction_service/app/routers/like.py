from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.crud.like import (
    count_likes_by_tweet,
    create_like,
    delete_like,
    get_like,
    get_likes_by_tweet,
)
from app.database.connection import get_session
from app.schemas.like import LikeBase, LikeCreate

router = APIRouter()


@router.get("/like/{tweet_id}")
def read_likes_by_tweet(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    likes_query = get_likes_by_tweet(session, tweet_id)
    if not likes_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No likes found."
        )
    return likes_query


@router.get("/like/{tweet_id}/count")
def count_likes_by_tweet_endpoint(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    likes_count_query = count_likes_by_tweet(tweet_id, session)
    if not likes_count_query:
        return JSONResponse(
            content={"total_likes": 0}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"total_likes": likes_count_query},
        status_code=status.HTTP_200_OK,
    )


@router.post("/like")
def create_like_endpoint(
    like: LikeCreate, session: Annotated[Session, Depends(get_session)]
):
    like_query = get_like(session, like.user_id, like.tweet_id)
    if like_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The like already exists.",
        )
    return create_like(session, like)


@router.delete("/like/{tweet_id}/{user_id}")
def delete_like_endpoint(
    tweet_id: int,
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    like_query = get_like(session, user_id, tweet_id)
    if not like_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Like not found."
        )
    tweet_owner = like_query["user_id"]
    if tweet_owner != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own likes.",
        )
    delete_like(
        session,
        LikeBase(
            user_id=like_query["user_id"], tweet_id=like_query["tweet_id"]
        ),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
