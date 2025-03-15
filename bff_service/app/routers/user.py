from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.auth import verify_token
from app.core.client import get_client
from app.core.config import SettingsDepends
from app.schemas.auth import UserUpdate

router = APIRouter(tags=["user"])


@router.get("/profile/")
async def get_profile(
    authorization: Annotated[dict, Depends(verify_token)],
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.get(
        f"{settings.AUTH_SERVICE_URL}/service_auth/users/profile/",
        headers={"Authorization": f"Bearer {authorization}"},
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.get("/users/")
async def get_users(settings: SettingsDepends):
    client = await get_client()
    response = await client.get(
        f"{settings.AUTH_SERVICE_URL}/service_auth/users/users_all/"
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )


@router.put("/profile/")
async def update_profile(
    authorization: Annotated[dict, Depends(verify_token)],
    update_data: UserUpdate,
    settings: SettingsDepends,
):
    client = await get_client()
    response = await client.put(
        f"{settings.AUTH_SERVICE_URL}/service_auth/users/profile/",
        headers={
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json",
        },
        json=update_data.model_dump(exclude_unset=True),
    )
    return JSONResponse(
        content=response.json(), status_code=response.status_code
    )
