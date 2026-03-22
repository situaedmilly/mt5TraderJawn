from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.proposal_review import ProposalReview
from app.db.models.trade_proposal import TradeProposal
from app.schemas.proposal import ProposalCreate, ProposalOut, ProposalReviewIn

router = APIRouter(prefix="/proposals", tags=["proposals"])


@router.post("", response_model=ProposalOut)
def create_proposal(payload: ProposalCreate, db: Session = Depends(get_db)) -> TradeProposal:
    row = TradeProposal(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[ProposalOut])
def list_proposals(db: Session = Depends(get_db)) -> list[TradeProposal]:
    return db.query(TradeProposal).order_by(TradeProposal.created_at.desc()).limit(100).all()


@router.post("/{proposal_id}/review")
def review_proposal(proposal_id: UUID, payload: ProposalReviewIn, db: Session = Depends(get_db)) -> dict:
    proposal = db.get(TradeProposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.proposal_status = payload.decision
    review = ProposalReview(
        proposal_id=proposal.id,
        decision=payload.decision,
        review_note=payload.review_note,
    )
    db.add(review)
    db.commit()
    return {"status": "ok", "proposal_id": str(proposal_id), "decision": payload.decision}
