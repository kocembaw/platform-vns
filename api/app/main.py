"""
FastAPI application -- read-only API over the synthetic experiment data

The data-generator creates the schema and seeds it; this service only reads
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import schemas
from .config import settings
from .db import get_db
from .models import Experiment, StimSession

# initialises fastapi app
app = FastAPI(title=settings.app_name)

# app health endopint
@app.get("/health")
def health():
    """Liveness probe / smoke-test target."""
    return {"status": "ok"}

# experimtents list endpoint
@app.get("/experiments", response_model=list[schemas.ExperimentSummary])
def list_experiments(db: Session = Depends(get_db)):
    rows = (
        db.query(Experiment, func.count(StimSession.id))
        .outerjoin(StimSession, StimSession.experiment_id == Experiment.id)
        .group_by(Experiment.id)
        .order_by(Experiment.id)
        .all()
    )
    return [
        schemas.ExperimentSummary(
            id=exp.id,
            protocol=exp.protocol,
            created_at=exp.created_at,
            session_count=count,
        )
        for exp, count in rows
    ]

# experiment details endpoint
@app.get("/experiments/{experiment_id}", response_model=schemas.ExperimentDetail)
def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    exp = db.get(Experiment, experiment_id)
    if exp is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return schemas.ExperimentDetail(
        id=exp.id,
        protocol=exp.protocol,
        description=exp.description,
        created_at=exp.created_at,
        session_count=len(exp.sessions),
        sessions=[schemas.SessionSummary.model_validate(s) for s in exp.sessions],
    )

# session details endpoint
@app.get("/sessions/{session_id}", response_model=schemas.SessionDetail)
def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.get(StimSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return schemas.SessionDetail.model_validate(session)
