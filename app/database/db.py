from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    url=settings.postgres_uri,
    echo=True,
)


def create_session(engine):
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )


session_local = create_session(engine)

Base = declarative_base()
