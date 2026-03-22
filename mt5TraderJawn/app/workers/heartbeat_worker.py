from app.core.db import SessionLocal
from app.services.heartbeat_service import write_heartbeat


def run_once() -> None:
    db = SessionLocal()
    try:
        row = write_heartbeat(
            db,
            service_name="api",
            instance_name="local-dev",
            status="online",
            message="heartbeat worker ping",
            json_metrics={"kind": "manual"},
        )
        print(f"Heartbeat written {row.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run_once()
