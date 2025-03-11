from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated, List
from sqlmodel import select

from crud.user import get_user_by_email, update_user_info
from database.connection import get_session
from models.user import Users
from schemas.user import UserUpdate
from utils.auth import decode_token

router = APIRouter()


@router.get("/profile/", tags=["Users"], response_model=Users)
def read_user(
    user: Annotated[dict, Depends(decode_token)],
    session: Session = Depends(get_session),
):
    user_id = get_user_by_email(session, user["email"]).id
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", tags=["Users"], response_model=List[Users])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(Users)).all()
    return users


@router.put("/profile/", tags=["Users"], response_model=Users)
def update_user(
    user: Annotated[dict, Depends(decode_token)],
    update_data: UserUpdate,
    session: Session = Depends(get_session),
):
    user_db = get_user_by_email(session, user["email"])
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user_info(
        session,
        user_db.id,
        new_name=update_data.name,
        new_password=update_data.password,
    )
    return updated_user
