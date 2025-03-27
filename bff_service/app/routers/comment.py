from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.comment import CommentCreate

router = APIRouter(tags=["comments"])


@router.get("/comments/tweet/{tweet_id}")
async def get_comments_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.INTERACTION_SERVICE_URL}/comments/{tweet_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/comments/tweet/{tweet_id}/count")
async def count_comments_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.INTERACTION_SERVICE_URL}/comments/{tweet_id}/count",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.post("/comment")
async def create_comment(
    comment_data: CommentCreate,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.INTERACTION_SERVICE_URL}/comments/{comment_data.tweet_id}",
        json={
            "user_id": authorization.get("uid"),
            "content": comment_data.content,
        },
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )
