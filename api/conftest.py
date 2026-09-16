"""
Test fixtures

Living at the api/ root, this conftest puts api/ on sys.path (so 'app' is
importable) and provides a TestClient backed by a shared in-memory SQLite
database seeded with one experiment and one session.
"""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    # StaticPool keeps a single connection, so the in-memory DB is shared
    # across sessions (otherwise each connection gets its own empty DB).
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    seed = TestingSessionLocal()
    seed.add(
        models.Experiment(
            id="exp-001",
            protocol="taVNS-A",
            description="demo",
            created_at=datetime.now(timezone.utc),
        )
    )
    seed.add(
        models.StimSession(
            id="sess-0001",
            experiment_id="exp-001",
            started_at=datetime.now(timezone.utc),
            duration_s=1200,
            mean_hr_bpm=68.4,
            hrv_rmssd_ms=42.1,
            hrv_sdnn_ms=55.3,
        )
    )
    seed.commit()
    seed.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
