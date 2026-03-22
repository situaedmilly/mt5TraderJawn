from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from app.api.deps import DatabaseSession
from app.db.models.heartbeat import Heartbeat
from app.schemas.heartbeat import HeartbeatCreate, HeartbeatResponse
from app.services.heartbeat_service import create_heartbeat
router = APIRouter()
@router.post("", response_model=HeartbeatResponse, status_code=201)
def create_heartbeat_endpoint(heartbeat_data: HeartbeatCreate, db: DatabaseSession):
    """Create a service heartbeat"""
    heartbeat = create_heartbeat(db, heartbeat_data)
    return heartbeat
@router.get("", response_model=List[HeartbeatResponse])
def list_heartbeats(db: DatabaseSession, limit: int = 50):
    """List recent heartbeats"""
    stmt = select(Heartbeat).order_by(Heartbeat.heartbeat_at.desc()).limit(limit)
    heartbeats = db.scalars(stmt).all()
    return heartbeats
