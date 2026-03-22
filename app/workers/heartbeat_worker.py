"""
Heartbeat worker
Sends periodic heartbeat to monitor service health.
Can be run as a cron job or background service.
"""
import logging
import socket
from datetime import datetime, timezone
from app.core.db import SessionLocal
from app.schemas.heartbeat import HeartbeatCreate
from app.services.heartbeat_service import create_heartbeat
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def send_heartbeat():
    """Send a heartbeat signal"""
    logger.info("Sending heartbeat")
    db = SessionLocal()
    try:
        hostname = socket.gethostname()
        heartbeat_data = HeartbeatCreate(
            service_name="scanner_worker",
            instance_name=hostname,
            status="healthy",
            message="Scanner worker active",
            json_metrics={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "hostname": hostname,
            },
        )
        create_heartbeat(db, heartbeat_data)
        logger.info("Heartbeat sent successfully")
    except Exception as e:
        logger.error(f"Heartbeat error: {e}", exc_info=True)
    finally:
        db.close()
if __name__ == "__main__":
    send_heartbeat()
