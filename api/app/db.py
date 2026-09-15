"""
database engine, session factory and the FastAPI dependency

The engine is created lazily (`create_engine` does not open a connection),
so importing this module never requires a running database - handy for tests.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# klasa bazowa, po której będą dziedziczyć wszystkie modele tabel w aplikacji
# SQLAlchemy wie, które klasy w Pythonie reprezentują tabele w bazie danych
Base = declarative_base()


def get_db():

    # otwiera nową sesję połączenia z bazą dla przychodzącego zapytania HTTP
    db = SessionLocal()
    try:
        # przekazuje ją do endpointu
        yield db
    finally:
        db.close()
