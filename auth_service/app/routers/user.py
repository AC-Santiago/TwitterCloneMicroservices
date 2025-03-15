from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session
from typing import Annotated, List
from sqlmodel import select

from app.crud.user import get_user_by_email, update_user_info
from app.database.connection import get_session
from app.models.user import Users
from app.schemas.user import UserResponse, UserUpdate
from app.utils.auth import decode_token

router = APIRouter()


@router.get("/profile/", tags=["Users"], response_model=Users)
def read_user(
    user: Annotated[dict, Depends(decode_token)],
    session: Session = Depends(get_session),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token invalido"
        )
    user_id = get_user_by_email(session, user["email"]).id
    user_query = session.get(Users, user_id)
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(
        content={
            "email": user_query.email,
            "name": user_query.name,
            "full_name": user_query.full_name,
            "biography": user_query.biography,
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/users_all/", tags=["Users"], response_model=List[UserResponse])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(Users)).all()
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            full_name=user.full_name,
            biography=user.biography,
        )
        for user in users
    ]


@router.put("/profile/", tags=["Users"], response_model=Users)
def update_user(
    user: Annotated[dict, Depends(decode_token)],
    update_data: UserUpdate,
    session: Session = Depends(get_session),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token invalido"
        )
    user_db = get_user_by_email(session, user["email"])
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user_info(
        session,
        user_db.id,
        user_update=update_data,
    )
    return updated_user
