
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String

from app.db.base import Base


class TradeProposal(Base):
    __tablename__ = "trade_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("signals.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    proposal_status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    order_type: Mapped[str] = mapped_column(String(16))
    proposed_entry: Mapped[float] = mapped_column(Numeric(18, 6))
    proposed_stop: Mapped[float] = mapped_column(Numeric(18, 6))
    proposed_tp1: Mapped[float] = mapped_column(Numeric(18, 6))
    lot_size: Mapped[float] = mapped_column(Numeric(12, 4))
    risk_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    expected_rr: Mapped[float] = mapped_column(Numeric(8, 4))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    policy_check_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    safety_check_passed: Mapped[bool] = mapped_column(Boolean, default=True)
