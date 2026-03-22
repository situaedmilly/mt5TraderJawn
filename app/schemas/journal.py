from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
class JournalCreate(BaseModel):
    """Schema for creating a manual trade journal entry"""
    signal_id: UUID
    taken: bool
    mt5_ticket: str | None = None
    actual_entry: Decimal | None = None
    actual_stop: Decimal | None = None
    actual_target: Decimal | None = None
    lot_size: Decimal | None = None
    risk_percent: Decimal | None = None
    result_status: str | None = None
    pnl_amount: Decimal | None = None
    notes: str | None = None
class JournalResponse(BaseModel):
    """Schema for journal response"""
    id: UUID
    signal_id: UUID
    taken: bool
    mt5_ticket: str | None
    actual_entry: Decimal | None
    actual_stop: Decimal | None
    actual_target: Decimal | None
    lot_size: Decimal | None
    risk_percent: Decimal | None
    result_status: str | None
    pnl_amount: Decimal | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
