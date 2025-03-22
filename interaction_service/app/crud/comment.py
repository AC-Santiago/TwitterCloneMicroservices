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

from app.models.interaction import Comments
from app.schemas.comment import CommentCreate


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


def _format_comment_response(row):
    if not row:
        return None
    return {
        "user_name": row.user_name,
        "tweet_id": row.Comments.tweet_id,
        "comment": row.Comments.content,
    }


def get_comment(db: Session, comment_id: int):
    _validate_ids(comment_id)
    users = _get_users_table().alias("users")
    comment = db.exec(
        select(Comments, users.c.name.label("user_name"))
        .join(users, users.c.id == Comments.user_id)
        .where(Comments.id == comment_id)
    ).first()
    return _format_comment_response(comment)


def get_comments_by_tweet(db: Session, tweet_id: int):
    _validate_ids(tweet_id)
    users = _get_users_table().alias("users")
    comments = db.exec(
        select(Comments, users.c.name.label("user_name"))
        .join(users, users.c.id == Comments.user_id)
        .where(Comments.tweet_id == tweet_id)
        .order_by(Comments.created_at.desc())
    ).all()
    return [_format_comment_response(comment) for comment in comments]


def count_comments_by_tweet(tweet_id: int, session: Session):
    total_comments = session.exec(
        select(func.count()).where(Comments.tweet_id == tweet_id)
    ).one()
    return total_comments


def create_comment(db: Session, comment: CommentCreate):
    _validate_ids(comment.user_id, comment.tweet_id)
    db_comment = Comments(
        user_id=comment.user_id,
        tweet_id=comment.tweet_id,
        content=comment.content,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return get_comment(db, db_comment.id)
