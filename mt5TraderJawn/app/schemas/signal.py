from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SignalCreate(BaseModel):
    strategy_id: UUID
    symbol_id: UUID
    signal_time: datetime
    session_name: str
    direction: str
    status: str = "new"
    priority_score: float = 0
    confidence_band: str = "B"
    htf_bias: str
    entry_tf: str
    entry_zone_low: float
    entry_zone_high: float
    stop_price: float
    target_1: float
    target_2: float | None = None
    expiry_time: datetime
    reason_code: str
    reason_text: str
    json_context: dict = Field(default_factory=dict)


class SignalOut(SignalCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
