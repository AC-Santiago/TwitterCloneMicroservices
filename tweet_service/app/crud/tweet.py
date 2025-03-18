from sqlmodel import Column, Integer, Session, String, Table, select, MetaData

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


def get_tweet(db: Session, tweet_id: int):
    if not isinstance(tweet_id, int) or tweet_id < 1:
        raise ValueError("The tweet ID must be a positive integer.")

    users = _get_users_table().alias("users")

    tweet_query = db.exec(
        select(Tweets, users.c.name.label("user_name"))
        .join(users, users.c.id == Tweets.user_id)
        .where(Tweets.id == tweet_id)
    ).first()

    return _format_tweet_response(tweet_query)


def get_tweets_by_user(db: Session, user_id: int):
    return db.exec(select(Tweets).where(Tweets.user_id == user_id)).all()


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
