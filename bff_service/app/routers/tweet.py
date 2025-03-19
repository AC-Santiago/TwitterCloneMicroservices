from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.tweet import TweetBase

router = APIRouter(tags=["tweets"])


@router.get("/tweets/{tweet_id}")
async def get_tweet(
    tweet_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/tweets/{tweet_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/tweets/")
async def get_tweets(
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/tweets/",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/tweets/user/{user_id}")
async def get_tweets_by_user(
    user_id: int,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.TWEET_SERVICE_URL}/tweets/user/{user_id}",
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.post("/tweet/")
async def create_tweet(
    tweet_data: TweetBase,
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.TWEET_SERVICE_URL}/tweet/",
        params={"user_id": authorization.get("uid")},
        json={
            "content": tweet_data.content,
            "user_id": authorization.get("uid"),
        },
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )
