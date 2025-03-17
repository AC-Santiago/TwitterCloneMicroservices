from sqlmodel import Session, select

from app.models.tweet import Retweets
from app.schemas.retweet import RetweetCreate


def create_retweet(db: Session, retweet: RetweetCreate):
    db_retweet = Retweets(user_id=retweet.user_id, tweet_id=retweet.tweet_id)
    db.add(db_retweet)
    db.commit()
    db.refresh(db_retweet)
    return db_retweet


def get_retweets_by_tweet(db: Session, tweet_id: int):
    return db.exec(select(Retweets).where(Retweets.tweet_id == tweet_id)).all()


def get_retweets_by_user(db: Session, user_id: int):
    return db.exec(select(Retweets).where(Retweets.user_id == user_id)).all()


def get_retweet(db: Session, user_id: int, tweet_id: int):
    return db.exec(
        select(Retweets)
        .where(Retweets.user_id == user_id)
        .where(Retweets.tweet_id == tweet_id)
    ).first()


def get_retweets(db: Session):
    return db.exec(select(Retweets)).all()
