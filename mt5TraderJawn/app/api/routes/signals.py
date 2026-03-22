from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.signal import Signal
from app.schemas.signal import SignalCreate, SignalOut

router = APIRouter(prefix="/signals", tags=["signals"])


@router.post("", response_model=SignalOut)
def create_signal(payload: SignalCreate, db: Session = Depends(get_db)) -> Signal:
    row = Signal(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[SignalOut])
def list_signals(db: Session = Depends(get_db)) -> list[Signal]:
    return db.query(Signal).order_by(Signal.created_at.desc()).limit(100).all()


@router.get("/{signal_id}", response_model=SignalOut)
def get_signal(signal_id: UUID, db: Session = Depends(get_db)) -> Signal:
    row = db.get(Signal, signal_id)
    if not row:
        raise HTTPException(status_code=404, detail="Signal not found")
    return row
