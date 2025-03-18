from sqlmodel import Session, text

from app.models.tweet import Retweets
from app.schemas.retweet import RetweetCreate


def create_retweet(db: Session, retweet: RetweetCreate):
    db_retweet = Retweets(user_id=retweet.user_id, tweet_id=retweet.tweet_id)
    db.add(db_retweet)
    db.commit()
    db.refresh(db_retweet)
    new_retweet = get_retweet(db, retweet.user_id, retweet.tweet_id)
    return new_retweet


def get_retweets_by_tweet(db: Session, tweet_id: int):
    query = text(
        """
        SELECT 
            r.tweet_id,
            r.user_id,
            u_retweeter.name as retweeter_name,
            t.content as tweet_content,
            u_author.name as author_name,
            r.created_at
        FROM retweets r
        INNER JOIN users u_retweeter ON u_retweeter.id = r.user_id
        INNER JOIN tweets t ON t.id = r.tweet_id
        INNER JOIN users u_author ON u_author.id = t.user_id
        WHERE r.tweet_id = :tweet_id
        ORDER BY r.created_at DESC
    """
    )
    results = db.exec(query, params={"tweet_id": tweet_id})
    return [
        {
            "tweet_id": row.tweet_id,
            "tweet_content": row.tweet_content,
            "author_name": row.author_name,
            "retweeter_name": row.retweeter_name,
            "created_at": row.created_at,
        }
        for row in results
    ]


def get_retweets_by_user(db: Session, user_id: int):
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError("user_id debe ser un número entero positivo")
    query = text(
        """
        SELECT 
            r.tweet_id,
            r.user_id,
            u_retweeter.name as retweeter_name,
            t.content as tweet_content,
            u_author.name as author_name,
            r.created_at
        FROM retweets r
        INNER JOIN users u_retweeter ON u_retweeter.id = r.user_id
        INNER JOIN tweets t ON t.id = r.tweet_id
        INNER JOIN users u_author ON u_author.id = t.user_id
        WHERE r.user_id = :user_id
        ORDER BY r.created_at DESC
    """
    )
    results = db.exec(query, params={"user_id": user_id})
    return [
        {
            "tweet_id": row.tweet_id,
            "tweet_content": row.tweet_content,
            "author_name": row.author_name,
            "retweeter_name": row.retweeter_name,
            "created_at": row.created_at,
        }
        for row in results
    ]


def get_retweet(db: Session, user_id: int, tweet_id: int):
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError("user_id debe ser un número entero positivo")
    if not isinstance(tweet_id, int) or tweet_id < 1:
        raise ValueError("tweet_id debe ser un número entero positivo")

    query = text(
        """
        SELECT 
            r.tweet_id,
            r.user_id,
            u_retweeter.name as retweeter_name,
            t.content as tweet_content,
            u_author.name as author_name,
            r.created_at
        FROM retweets r
        INNER JOIN users u_retweeter ON u_retweeter.id = r.user_id
        INNER JOIN tweets t ON t.id = r.tweet_id
        INNER JOIN users u_author ON u_author.id = t.user_id
        WHERE r.user_id = :user_id AND r.tweet_id = :tweet_id
    """
    )
    results = db.exec(query, params={"user_id": user_id, "tweet_id": tweet_id})
    result = results.first()
    if result:
        return {
            "tweet_id": result.tweet_id,
            "tweet_content": result.tweet_content,
            "author_name": result.author_name,
            "retweeter_name": result.retweeter_name,
            "created_at": result.created_at,
        }
    return None


def get_retweets(db: Session):
    query = text(
        """
        SELECT 
            r.tweet_id,
            r.user_id,
            u_retweeter.name as retweeter_name,
            t.content as tweet_content,
            u_author.name as author_name,
            r.created_at
        FROM retweets r
        INNER JOIN users u_retweeter ON u_retweeter.id = r.user_id
        INNER JOIN tweets t ON t.id = r.tweet_id
        INNER JOIN users u_author ON u_author.id = t.user_id
        ORDER BY r.created_at DESC
    """
    )
    results = db.exec(query)
    return [
        {
            "tweet_id": row.tweet_id,
            "tweet_content": row.tweet_content,
            "author_name": row.author_name,
            "retweeter_name": row.retweeter_name,
            "created_at": row.created_at,
        }
        for row in results
    ]
