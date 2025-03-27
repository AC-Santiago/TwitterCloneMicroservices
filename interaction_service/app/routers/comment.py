from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.datastructures import Default
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.crud.comment import (
    count_comments_by_tweet,
    create_comment,
    get_comment,
    get_comments_by_tweet,
)
from app.database.connection import get_session
from app.schemas.comment import CommentBase, CommentCreate

router = APIRouter()


@router.get("/comments/{tweet_id}")
def read_comments_by_tweet(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    comments_query = get_comments_by_tweet(session, tweet_id)
    return comments_query


@router.get("/comments/{tweet_id}/count")
def count_comments_by_tweet_endpoint(
    tweet_id: int, session: Annotated[Session, Depends(get_session)]
):
    comments_count_query = count_comments_by_tweet(tweet_id, session)
    if not comments_count_query:
        return JSONResponse(
            content={"total_comments": 0}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"total_comments": comments_count_query},
        status_code=status.HTTP_200_OK,
    )


@router.post("/comments/{tweet_id}")
def create_comment_endpoint(
    tweet_id: int,
    comment: CommentBase,
    session: Annotated[Session, Depends(get_session)],
):
    new_comment = CommentCreate(
        content=comment.content,
        user_id=comment.user_id,
        tweet_id=tweet_id,
    )
    return create_comment(session, new_comment)
