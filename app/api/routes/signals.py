from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DatabaseSession
from app.db.models.signal import Signal
from app.schemas.signal import SignalCreate, SignalResponse
router = APIRouter()
@router.post("", response_model=SignalResponse, status_code=201)
def create_signal(signal_data: SignalCreate, db: DatabaseSession):
    """Create a new trading signal"""
    signal = Signal(**signal_data.model_dump())
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal
@router.get("", response_model=List[SignalResponse])
def list_signals(
    db: DatabaseSession,
    status: str | None = None,
    limit: int = 100,
):
    """List trading signals with optional filtering"""
    stmt = select(Signal).order_by(Signal.signal_time.desc())
    if status:
        stmt = stmt.where(Signal.status == status)
    stmt = stmt.limit(limit)
    signals = db.scalars(stmt).all()
    return signals
@router.get("/{signal_id}", response_model=SignalResponse)
def get_signal(signal_id: UUID, db: DatabaseSession):
    """Get a specific signal by ID"""
    signal = db.get(Signal, signal_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal
