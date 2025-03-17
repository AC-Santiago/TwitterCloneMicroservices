from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.client import get_client
from app.core.config import SettingsDepends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/service_auth/auth/login")


async def verify_token(
    settings: SettingsDepends,
    authorization: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    """
    Verifica el token JWT consultando al auth_service y retorna la información del usuario
    si el token es válido.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization header is required",
        )

    client = await get_client()
    response = await client.get(
        f"{settings.AUTH_SERVICE_URL}/service_auth/verify_token",
        headers={"Authorization": f"Bearer {authorization}"},
    )
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.json().get("detail"),
        )

    return response.json()
