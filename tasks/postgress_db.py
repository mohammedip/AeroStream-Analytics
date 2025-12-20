# tasks/postgres_db.py

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    func,
    JSON
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime


DATABASE_URL = (
    "postgresql+psycopg2://aerostream:aerostream@postgres:5432/aerostream_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()

class TweetPrediction(Base):
    __tablename__ = "tweet_predictions"

    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)
    original_confidence = Column(Float)
    negative_reason = Column(String)
    predicted_sentiment = Column(String, nullable=False)
    probabilities = Column(JSON)
    inserted_at = Column(DateTime, server_default=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)


def store_predictions(predictions: list[dict]) -> None:
    session = SessionLocal()
    try:
        rows = [
            TweetPrediction(
                airline=t["airline"],
                text=t["text"],
                created_at=datetime.fromisoformat(t["tweet_created"]),
                original_confidence=t["airline_sentiment_confidence"],
                negative_reason=t["negativereason"],
                predicted_sentiment=t["predicted_sentiment"],
                probabilities=t["sentiment_probabilities"],
            )
            for t in predictions
        ]

        session.bulk_save_objects(rows)
        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def total_tweets() -> int:
    session = SessionLocal()
    try:
        return session.query(func.count(TweetPrediction.id)).scalar()
    finally:
        session.close()


def tweets_by_airline():
    session = SessionLocal()
    try:
        return (
            session.query(
                TweetPrediction.airline,
                func.count(TweetPrediction.id)
            )
            .group_by(TweetPrediction.airline)
            .order_by(func.count(TweetPrediction.id).desc())
            .all()
        )
    finally:
        session.close()


def sentiment_distribution():
    session = SessionLocal()
    try:
        return (
            session.query(
                TweetPrediction.predicted_sentiment,
                func.count(TweetPrediction.id)
            )
            .group_by(TweetPrediction.predicted_sentiment)
            .all()
        )
    finally:
        session.close()


def negative_reasons():
    session = SessionLocal()
    try:
        return (
            session.query(
                TweetPrediction.negative_reason,
                func.count(TweetPrediction.id)
            )
            .filter(
                TweetPrediction.predicted_sentiment == "negative",
                TweetPrediction.negative_reason.isnot(None),
            )
            .group_by(TweetPrediction.negative_reason)
            .order_by(func.count(TweetPrediction.id).desc())
            .all()
        )
    finally:
        session.close()
