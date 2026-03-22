from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models.heartbeat import Heartbeat
from app.schemas.heartbeat import HeartbeatCreate
def create_heartbeat(db: Session, heartbeat_data: HeartbeatCreate) -> Heartbeat:
    """
    Create a heartbeat record

    Args:
        db: Database session
        heartbeat_data: Heartbeat creation schema

    Returns:
        Heartbeat: Created heartbeat instance
    """
    heartbeat = Heartbeat(
        service_name=heartbeat_data.service_name,
        instance_name=heartbeat_data.instance_name,
        status=heartbeat_data.status,
        heartbeat_at=datetime.now(timezone.utc),
        message=heartbeat_data.message,
        json_metrics=heartbeat_data.json_metrics,
    )
    db.add(heartbeat)
    db.commit()
    db.refresh(heartbeat)
    return heartbeat
