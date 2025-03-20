from sqlmodel import (
    Column,
    Integer,
    MetaData,
    Session,
    String,
    Table,
    func,
    select,
)

from app.models.interaction import Likes
from app.schemas.like import LikeBase, LikeCreate


def _validate_ids(*ids):
    for id_value in ids:
        if not isinstance(id_value, int) or id_value < 1:
            raise ValueError("The ID must be a positive integer.")


def _get_users_table():
    metadata = MetaData()
    return Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )


def _format_like_response(row):
    if not row:
        return None
    return {
        "user_name": row.user_name,
        "user_id": row.Likes.user_id,
        "tweet_id": row.Likes.tweet_id,
    }


def get_like(db: Session, user_id: int, tweet_id: int):
    _validate_ids(user_id, tweet_id)
    user = _get_users_table().alias("user")
    like = db.exec(
        select(Likes, user.c.name.label("user_name"))
        .join(user, user.c.id == Likes.user_id)
        .where(Likes.tweet_id == tweet_id)
        .where(Likes.user_id == user_id)
    ).first()
    return _format_like_response(like)


def get_likes_by_tweet(db: Session, tweet_id: int):
    _validate_ids(tweet_id)
    users = _get_users_table().alias("users")
    likes = db.exec(
        select(Likes, users.c.name.label("user_name"))
        .join(users, users.c.id == Likes.user_id)
        .where(Likes.tweet_id == tweet_id)
    ).all()
    return [_format_like_response(like) for like in likes]


def get_likes_by_user(db: Session, user_id: int):
    return db.exec(select(Likes).where(Likes.user_id == user_id)).all()


def count_likes_by_tweet(tweet_id: int, session: Session):
    total_likes = session.exec(
        select(func.count()).where(Likes.tweet_id == tweet_id)
    ).one()
    return total_likes


def create_like(db: Session, like: LikeCreate):
    _validate_ids(like.user_id, like.tweet_id)
    db_like = Likes(user_id=like.user_id, tweet_id=like.tweet_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return get_like(db, like.user_id, like.tweet_id)


def delete_like(db: Session, like: LikeBase):
    like = db.get(Likes, (like.tweet_id, like.user_id))
    if like:
        db.delete(like)
        db.commit()
    return like
