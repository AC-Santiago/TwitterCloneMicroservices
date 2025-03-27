from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Header
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.auth import UserCreate


router = APIRouter(tags=["auth"])


@router.post("/auth/register")
async def register(
    user_data: UserCreate,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.AUTH_SERVICE_URL}/service_auth/register",
        json=user_data.__dict__,
    )
    return JSONResponse(response.json(), status_code=response.status_code)


@router.post("/auth/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.AUTH_SERVICE_URL}/service_auth/login",
        data={
            "username": form_data.username,
            "password": form_data.password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/auth/verify_token")
async def verify_token(
    authorization: Annotated[dict, Depends(verify_token)],
):
    return authorization


@router.post("/auth/logout")
async def logout(
    authorization: Annotated[str, Header(..., alias="Authorization")],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.post(
        f"{settings.AUTH_SERVICE_URL}/service_auth/logout",
        headers={"Authorization": authorization},
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )
