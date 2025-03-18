from sqlmodel import Column, Integer, MetaData, Session, String, Table, select

from app.models.tweet import Retweets, Tweets
from app.schemas.retweet import RetweetCreate


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


def _format_retweet_response(row):
    return {
        "tweet_id": row.Retweets.tweet_id,
        "tweet_content": row.tweet_content,
        "author_name": row.author_name,
        "retweeter_name": row.retweeter_name,
        "created_at": row.Retweets.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


def create_retweet(db: Session, retweet: RetweetCreate):
    _validate_ids(retweet.user_id, retweet.tweet_id)
    db_retweet = Retweets(user_id=retweet.user_id, tweet_id=retweet.tweet_id)
    db.add(db_retweet)
    db.commit()
    db.refresh(db_retweet)
    return get_retweet(db, retweet.user_id, retweet.tweet_id)


def get_retweets_by_tweet(db: Session, tweet_id: int):
    _validate_ids(tweet_id)
    retweeter = _get_users_table().alias("retweeter")
    author = _get_users_table().alias("author")

    query = (
        select(
            Retweets,
            Tweets.content.label("tweet_content"),
            retweeter.c.name.label("retweeter_name"),
            author.c.name.label("author_name"),
        )
        .join(retweeter, retweeter.c.id == Retweets.user_id)
        .join(Tweets, Tweets.id == Retweets.tweet_id)
        .join(author, author.c.id == Tweets.user_id, isouter=True)
        .where(Retweets.tweet_id == tweet_id)
        .order_by(Retweets.created_at.desc())
    )

    results = db.exec(query)
    return [_format_retweet_response(row) for row in results]


def get_retweets_by_user(db: Session, user_id: int):
    _validate_ids(user_id)
    retweeter = _get_users_table().alias("retweeter")
    author = _get_users_table().alias("author")

    query = (
        select(
            Retweets,
            Tweets.content.label("tweet_content"),
            retweeter.c.name.label("retweeter_name"),
            author.c.name.label("author_name"),
        )
        .join(retweeter, retweeter.c.id == Retweets.user_id)
        .join(Tweets, Tweets.id == Retweets.tweet_id)
        .join(author, author.c.id == Tweets.user_id, isouter=True)
        .where(Retweets.user_id == user_id)
        .order_by(Retweets.created_at.desc())
    )

    results = db.exec(query)
    return [_format_retweet_response(row) for row in results]


def get_retweet(db: Session, user_id: int, tweet_id: int):
    _validate_ids(user_id, tweet_id)
    retweeter = _get_users_table().alias("retweeter")
    author = _get_users_table().alias("author")

    query = (
        select(
            Retweets,
            Tweets.content.label("tweet_content"),
            retweeter.c.name.label("retweeter_name"),
            author.c.name.label("author_name"),
        )
        .join(retweeter, retweeter.c.id == Retweets.user_id)
        .join(Tweets, Tweets.id == Retweets.tweet_id)
        .join(author, author.c.id == Tweets.user_id, isouter=True)
        .where(Retweets.user_id == user_id, Retweets.tweet_id == tweet_id)
    )

    result = db.exec(query).first()
    return _format_retweet_response(result) if result else None


def get_retweets(db: Session):
    retweeter = _get_users_table().alias("retweeter")
    author = _get_users_table().alias("author")

    query = (
        select(
            Retweets,
            Tweets.content.label("tweet_content"),
            retweeter.c.name.label("retweeter_name"),
            author.c.name.label("author_name"),
        )
        .join(retweeter, retweeter.c.id == Retweets.user_id)
        .join(Tweets, Tweets.id == Retweets.tweet_id)
        .join(author, author.c.id == Tweets.user_id, isouter=True)
        .order_by(Retweets.created_at.desc())
    )

    results = db.exec(query)
    return [_format_retweet_response(row) for row in results]
