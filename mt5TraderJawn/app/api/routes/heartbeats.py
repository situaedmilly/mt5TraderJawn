from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.heartbeat import Heartbeat
from app.schemas.heartbeat import HeartbeatCreate, HeartbeatOut

router = APIRouter(prefix="/heartbeats", tags=["heartbeats"])


@router.get("", response_model=list[HeartbeatOut])
def list_heartbeats(db: Session = Depends(get_db)) -> list[Heartbeat]:
    return db.query(Heartbeat).order_by(Heartbeat.heartbeat_at.desc()).limit(100).all()


@router.post("", response_model=HeartbeatOut)
def create_heartbeat(payload: HeartbeatCreate, db: Session = Depends(get_db)) -> Heartbeat:
    row = Heartbeat(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
