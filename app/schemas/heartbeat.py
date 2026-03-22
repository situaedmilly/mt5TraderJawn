from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
class HeartbeatCreate(BaseModel):
    """Schema for creating a heartbeat"""
    service_name: str
    instance_name: str
    status: str
    message: str | None = None
    json_metrics: dict | None = None
class HeartbeatResponse(BaseModel):
    """Schema for heartbeat response"""
    id: UUID
    service_name: str
    instance_name: str
    status: str
    heartbeat_at: datetime
    message: str | None
    json_metrics: dict | None
    model_config = {"from_attributes": True}
