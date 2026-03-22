from datetime import datetime, timezone
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DatabaseSession
from app.db.models.trade_proposal import TradeProposal
from app.db.models.proposal_review import ProposalReview
from app.schemas.proposal import (
    ProposalCreate,
    ProposalResponse,
    ProposalReviewCreate,
    ProposalReviewResponse,
)
router = APIRouter()
@router.post("", response_model=ProposalResponse, status_code=201)
def create_proposal(proposal_data: ProposalCreate, db: DatabaseSession):
    """Create a new trade proposal"""
    proposal = TradeProposal(**proposal_data.model_dump())
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal
@router.get("", response_model=List[ProposalResponse])
def list_proposals(
    db: DatabaseSession,
    status: str | None = None,
    limit: int = 100,
):
    """List trade proposals with optional filtering"""
    stmt = select(TradeProposal).order_by(TradeProposal.created_at.desc())
    if status:
        stmt = stmt.where(TradeProposal.proposal_status == status)
    stmt = stmt.limit(limit)
    proposals = db.scalars(stmt).all()
    return proposals
@router.post("/{proposal_id}/review", response_model=ProposalReviewResponse, status_code=201)
def review_proposal(
    proposal_id: UUID,
    review_data: ProposalReviewCreate,
    db: DatabaseSession,
):
    """Review and approve/reject a trade proposal"""
    proposal = db.get(TradeProposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    # Update proposal status based on decision
    if review_data.decision == "approved":
        proposal.proposal_status = "approved"
    elif review_data.decision == "rejected":
        proposal.proposal_status = "rejected"
    # Create review record
    review = ProposalReview(
        proposal_id=proposal_id,
        decision=review_data.decision,
        review_note=review_data.review_note,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
