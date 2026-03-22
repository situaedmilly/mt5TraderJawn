from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
class SignalCreate(BaseModel):
    """Schema for creating a signal"""
    strategy_id: UUID
    symbol_id: UUID
    signal_time: datetime
    direction: str = Field(..., pattern="^(long|short)$")
    session_name: str | None = None
    priority_score: float | None = None
    confidence_band: str | None = None
    htf_bias: str | None = None
    entry_tf: str | None = None
    entry_zone_low: Decimal | None = None
    entry_zone_high: Decimal | None = None
    stop_price: Decimal | None = None
    target_1: Decimal | None = None
    target_2: Decimal | None = None
    expiry_time: datetime | None = None
    reason_code: str | None = None
    reason_text: str | None = None
    json_context: dict | None = None
class SignalResponse(BaseModel):
    """Schema for signal response"""
    id: UUID
    strategy_id: UUID
    symbol_id: UUID
    created_at: datetime
    updated_at: datetime
    signal_time: datetime
    session_name: str | None
    direction: str
    status: str
    priority_score: float | None
    confidence_band: str | None
    htf_bias: str | None
    entry_tf: str | None
    entry_zone_low: Decimal | None
    entry_zone_high: Decimal | None
    stop_price: Decimal | None
    target_1: Decimal | None
    target_2: Decimal | None
    expiry_time: datetime | None
    reason_code: str | None
    reason_text: str | None
    json_context: dict | None
    model_config = {"from_attributes": True}
