from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HeartbeatCreate(BaseModel):
    service_name: str
    instance_name: str
    status: str
    message: str | None = None
    json_metrics: dict = Field(default_factory=dict)


class HeartbeatOut(HeartbeatCreate):
    id: UUID
    heartbeat_at: datetime

    model_config = ConfigDict(from_attributes=True)
