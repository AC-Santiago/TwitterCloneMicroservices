from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.like import LikeCreate, LikeBase

router = APIRouter(tags=["likes"])


@router.get("/likes/tweet/{tweet_id}")
async def get_likes_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.INTERACTION_SERVICE_URL}/like/{tweet_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/likes/tweet/{tweet_id}/count")
async def count_likes_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.INTERACTION_SERVICE_URL}/like/{tweet_id}/count",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.post("/like")
async def create_like(
    like_data: LikeCreate,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.INTERACTION_SERVICE_URL}/like",
        json={
            "user_id": authorization.get("uid"),
            "tweet_id": like_data.tweet_id,
        },
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.delete("/like/")
async def delete_like(
    like: LikeBase,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.delete(
        f"{settings.INTERACTION_SERVICE_URL}/like/{like.tweet_id}/{authorization.get('uid')}",
    )
    if response.status_code == 404:
        return JSONResponse(
            content={"detail": "Like not found."},
            status_code=response.status_code,
        )
    return Response(
        status_code=response.status_code,
    )
