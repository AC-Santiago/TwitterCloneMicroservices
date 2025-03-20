from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


session_dep = Annotated[Session, Depends(get_session)]
