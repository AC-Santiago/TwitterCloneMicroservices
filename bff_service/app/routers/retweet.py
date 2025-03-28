from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.retweet import RetweetCreate

router = APIRouter(tags=["retweets"])


@router.get("/retweets/{tweet_id}")
async def get_retweets_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/retweets/{tweet_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/retweets/")
async def get_retweets(
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/retweets/",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/retweets/user/{user_id}")
async def get_retweets_by_user(
    user_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/retweets/user/{user_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/retweets/count/tweet/{tweet_id}")
async def get_retweets_count_by_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/retweets/count/tweet/{tweet_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.post("/retweet/")
async def create_retweet(
    retweet_data: RetweetCreate,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.TWEET_SERVICE_URL}/retweet/",
        json={
            "user_id": authorization.get("uid"),
            "tweet_id": retweet_data.tweet_id,
        },
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.delete("/retweet/{tweet_id}")
async def delete_retweet(
    tweet_id: int,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.delete(
        f"{settings.TWEET_SERVICE_URL}/retweet/{authorization.get('uid')}/{tweet_id}",
    )
    return Response(
        status_code=response.status_code,
    )
