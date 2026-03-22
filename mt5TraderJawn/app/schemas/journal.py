from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class JournalCreate(BaseModel):
    signal_id: UUID
    taken: bool = False
    mt5_ticket: str | None = None
    actual_entry: float | None = None
    actual_stop: float | None = None
    actual_target: float | None = None
    lot_size: float | None = None
    risk_percent: float | None = None
    result_status: str = "open"
    pnl_amount: float | None = None
    notes: str | None = None


class JournalOut(JournalCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
