"""SQLAlchemy ORM models.

Mirrors what the data-generator writes: experiments group stimulation
sessions, and each session carries synthetic (fabricated) biosignal metrics.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    protocol: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    sessions: Mapped[list["StimSession"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan"
    )


class StimSession(Base):
    # Named StimSession to avoid clashing with SQLAlchemy's own Session.
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id"), index=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_s: Mapped[int] = mapped_column(Integer)

    # --- synthetic metrics (fabricated, not real measurements) ---
    mean_hr_bpm: Mapped[float] = mapped_column(Float)
    hrv_rmssd_ms: Mapped[float] = mapped_column(Float)
    hrv_sdnn_ms: Mapped[float] = mapped_column(Float)

    experiment: Mapped["Experiment"] = relationship(back_populates="sessions")
