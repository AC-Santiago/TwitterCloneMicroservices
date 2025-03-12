from datetime import datetime, timedelta, timezone

from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import Depends

from app.core.config import SettingsDepends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def encode_token(
    payload: dict,
    settings: SettingsDepends,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode: dict = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(
    token: Annotated[str, Depends(oauth2_scheme)], settings: SettingsDepends
) -> dict:
    return jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
