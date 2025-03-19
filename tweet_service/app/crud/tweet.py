from sqlmodel import Column, Integer, Session, String, Table, select, MetaData

from app.crud.retweet import get_retweets_by_user
from app.models.tweet import Tweets
from app.schemas.tweet import TweetCreate


def _format_tweet_response(row):
    if not row:
        return None
    return {
        "id": row.Tweets.id,
        "content": row.Tweets.content,
        "created_at": row.Tweets.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": row.user_name,
    }


def _get_users_table():
    metadata = MetaData()
    return Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )


def _validate_id(id: int):
    if not isinstance(id, int) or id < 1:
        raise ValueError("The tweet ID must be a positive integer.")


def get_tweets_retweeted_by_user(db: Session, user_id: int):
    _validate_id(user_id)
    tweets_by_user = get_tweets_by_user(db, user_id)
    retweets = get_retweets_by_user(db, user_id)

    tweets_retweeted = tweets_by_user + retweets
    tweets_retweeted.sort(key=lambda x: x["created_at"], reverse=True)
    return tweets_retweeted


def get_tweet(db: Session, tweet_id: int):
    _validate_id(tweet_id)
    users = _get_users_table().alias("users")

    tweet_query = db.exec(
        select(Tweets, users.c.name.label("user_name"))
        .join(users, users.c.id == Tweets.user_id)
        .where(Tweets.id == tweet_id)
    ).first()

    return _format_tweet_response(tweet_query)


def get_tweets_by_user(db: Session, user_id: int):
    users = _get_users_table().alias("users")
    results = db.exec(
        select(Tweets, users.c.name.label("user_name"))
        .join(users, users.c.id == Tweets.user_id)
        .where(Tweets.user_id == user_id)
        .order_by(Tweets.id.desc())
    )
    return [_format_tweet_response(row) for row in results]


def create_tweet(db: Session, tweet: TweetCreate):
    db_tweet = Tweets(user_id=tweet.user_id, content=tweet.content)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    new_tweet = get_tweet(db, db_tweet.id)
    return new_tweet


def get_tweets(session: Session):
    users = _get_users_table().alias("users")

    results = session.exec(
        select(Tweets, users.c.name.label("user_name"))
        .join(users, users.c.id == Tweets.user_id)
        .order_by(Tweets.id.desc())
    )
    return [_format_tweet_response(row) for row in results]
