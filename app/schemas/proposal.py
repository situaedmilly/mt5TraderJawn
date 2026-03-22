from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
class ProposalCreate(BaseModel):
    """Schema for creating a trade proposal"""
    signal_id: UUID
    order_type: str
    proposed_entry: Decimal
    proposed_stop: Decimal
    proposed_tp1: Decimal | None = None
    lot_size: Decimal
    risk_percent: Decimal
    expected_rr: Decimal | None = None
    expires_at: datetime | None = None
class ProposalResponse(BaseModel):
    """Schema for proposal response"""
    id: UUID
    signal_id: UUID
    created_at: datetime
    updated_at: datetime
    proposal_status: str
    order_type: str
    proposed_entry: Decimal
    proposed_stop: Decimal
    proposed_tp1: Decimal | None
    lot_size: Decimal
    risk_percent: Decimal
    expected_rr: Decimal | None
    expires_at: datetime | None
    policy_check_passed: bool
    safety_check_passed: bool
    model_config = {"from_attributes": True}
class ProposalReviewCreate(BaseModel):
    """Schema for reviewing a proposal"""
    decision: str
    review_note: str | None = None
class ProposalReviewResponse(BaseModel):
    """Schema for proposal review response"""
    id: UUID
    proposal_id: UUID
    decision: str
    decision_time: datetime
    review_note: str | None
    model_config = {"from_attributes": True}
