from sqlalchemy.orm import Session

from app.db.models.heartbeat import Heartbeat


def write_heartbeat(
    db: Session,
    service_name: str,
    instance_name: str,
    status: str,
    message: str | None = None,
    json_metrics: dict | None = None,
) -> Heartbeat:
    row = Heartbeat(
        service_name=service_name,
        instance_name=instance_name,
        status=status,
        message=message,
        json_metrics=json_metrics or {},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
