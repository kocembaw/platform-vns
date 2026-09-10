"""Seed the database with synthetic taVNS experiment data.

Deterministic: the same SEED always produces exactly the same rows, which is
what makes demos and tests repeatable. Everything here is fabricated — there
are no real measurements.

This script also OWNS THE SCHEMA: it creates the tables the API reads from.
The table definitions below must stay in sync with api/app/models.py.

Environment variables:
  DATABASE_URL    SQLAlchemy URL (default: local docker-compose Postgres)
  SEED            RNG seed (default: 42)
  N_EXPERIMENTS   how many experiments to create (default: 5)
  RESET           wipe existing rows before seeding (default: true)
"""

import os
import time
from datetime import datetime, timedelta, timezone

import yaml
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
    text,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://vns:vns@db:5432/vns"
)
SEED = int(os.environ.get("SEED", "42"))
N_EXPERIMENTS = int(os.environ.get("N_EXPERIMENTS", "5"))
RESET = os.environ.get("RESET", "true").lower() in ("1", "true", "yes")

PROTOCOLS_PATH = os.path.join(os.path.dirname(__file__), "protocols.yaml")

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True)
    protocol = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship(
        "StimSession", back_populates="experiment", cascade="all, delete-orphan"
    )


class StimSession(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    experiment_id = Column(String, ForeignKey("experiments.id"), index=True)
    started_at = Column(DateTime(timezone=True))
    duration_s = Column(Integer)
    mean_hr_bpm = Column(Float)
    hrv_rmssd_ms = Column(Float)
    hrv_sdnn_ms = Column(Float)

    experiment = relationship("Experiment", back_populates="sessions")


def load_protocols(path: str) -> list[dict]:
    with open(path) as handle:
        return yaml.safe_load(handle)["protocols"]


def build_rows(protocols: list[dict]):
    """Build experiment and session rows deterministically."""
    experiments: list[Experiment] = []
    sessions: list[StimSession] = []
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)

    for i in range(1, N_EXPERIMENTS + 1):
        proto = protocols[(i - 1) % len(protocols)]  # deterministic assignment
        exp_id = f"exp-{i:03d}"
        experiments.append(
            Experiment(
                id=exp_id,
                protocol=proto["name"],
                description=proto.get("description"),
                created_at=base_time + timedelta(days=i),
            )
        )

        n_sessions = random.randint(*proto["sessions_per_experiment"])
        for j in range(1, n_sessions + 1):
            sessions.append(
                StimSession(
                    id=f"{exp_id}-s{j:03d}",
                    experiment_id=exp_id,
                    started_at=base_time + timedelta(days=i, hours=j),
                    duration_s=random.randint(*proto["duration_s"]),
                    mean_hr_bpm=round(random.uniform(*proto["mean_hr_bpm"]), 1),
                    hrv_rmssd_ms=round(random.uniform(*proto["hrv_rmssd_ms"]), 1),
                    hrv_sdnn_ms=round(random.uniform(*proto["hrv_sdnn_ms"]), 1),
                )
            )
    return experiments, sessions


def wait_for_db(engine, attempts: int = 30, delay: int = 2) -> None:
    """Retry until Postgres accepts connections (it may start after us)."""
    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            print(f"DB not ready (attempt {attempt}/{attempts}); retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError(f"Database not reachable after {attempts} attempts")


def main() -> None:
    random.seed(SEED)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
    wait_for_db(engine)
    Base.metadata.create_all(engine)

    protocols = load_protocols(PROTOCOLS_PATH)
    experiments, sessions = build_rows(protocols)

    Session = sessionmaker(bind=engine, future=True)
    with Session() as db:
        if RESET:
            db.query(StimSession).delete()
            db.query(Experiment).delete()
            db.commit()
        elif db.query(Experiment).count() > 0:
            print("Data already present; set RESET=true to reseed. Skipping.")
            return

        db.add_all(experiments)
        db.add_all(sessions)
        db.commit()

    print(
        f"Seeded {len(experiments)} experiments and {len(sessions)} sessions "
        f"(seed={SEED})."
    )


if __name__ == "__main__":
    main()
