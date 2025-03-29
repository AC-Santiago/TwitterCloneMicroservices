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


def _get_tweets_table():
    metadata = MetaData()
    return Table(
        "tweets",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("content", String),
        Column("created_at", String),
        Column("user_id", Integer),
    )


def _format_like_response(row):
    if not row:
        return None
    return {
        "user_name": row.user_name,
        "user_id": row.Likes.user_id,
        "tweet_id": row.Likes.tweet_id,
    }


def _format_tweet_response(row):
    if not row:
        return None
    return {
        "id": row.id,
        "content": row.content,
        "created_at": row.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": row.author_name,
        "author_name": row.user_name,
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
    tweets = _get_tweets_table().alias("tweets")
    users = _get_users_table().alias("users")
    tweet_authors = _get_users_table().alias("tweet_authors")
    likes = db.exec(
        select(
            Likes,
            tweets,
            users.c.name.label("user_name"),
            tweet_authors.c.name.label("author_name"),
        )
        .join(tweets, tweets.c.id == Likes.tweet_id)
        .join(users, users.c.id == Likes.user_id)
        .join(tweet_authors, tweet_authors.c.id == tweets.c.user_id)
        .where(Likes.user_id == user_id)
    ).all()
    return [_format_tweet_response(like) for like in likes]


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
