from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProposalCreate(BaseModel):
    signal_id: UUID
    order_type: str
    proposed_entry: float
    proposed_stop: float
    proposed_tp1: float
    lot_size: float
    risk_percent: float
    expected_rr: float
    expires_at: datetime
    policy_check_passed: bool = True
    safety_check_passed: bool = True


class ProposalOut(ProposalCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    proposal_status: str

    model_config = ConfigDict(from_attributes=True)


class ProposalReviewIn(BaseModel):
    decision: str
    review_note: str | None = None
