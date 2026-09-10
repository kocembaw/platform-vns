"""Pydantic response models (validation & serialization)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    started_at: datetime
    duration_s: int


class SessionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    experiment_id: str
    started_at: datetime
    duration_s: int
    mean_hr_bpm: float
    hrv_rmssd_ms: float
    hrv_sdnn_ms: float


class ExperimentSummary(BaseModel):
    id: str
    protocol: str
    created_at: datetime
    session_count: int


class ExperimentDetail(BaseModel):
    id: str
    protocol: str
    description: str | None
    created_at: datetime
    session_count: int
    sessions: list[SessionSummary]
