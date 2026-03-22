
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
from sqlalchemy import DateTime, ForeignKey, String, Text

from app.db.base import Base


class ProposalReview(Base):
    __tablename__ = "proposal_reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trade_proposals.id"), index=True)
    decision: Mapped[str] = mapped_column(String(16))
    decision_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
