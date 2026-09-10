"""Database engine, session factory and the FastAPI dependency.

The engine is created lazily (``create_engine`` does not open a connection),
so importing this module never requires a running database - handy for tests.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_db():
    """Yield a database session, closing it when the request is done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
