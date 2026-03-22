from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class TradeProposal(Base):
    """Trade proposal for Phase 2 semi-automated workflow"""
    __tablename__ = "trade_proposals"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    signal_id: Mapped[UUID] = mapped_column(ForeignKey("signals.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    proposal_status: Mapped[str] = mapped_column(String(20), default="pending", index=True, nullable=False)
    order_type: Mapped[str] = mapped_column(String(20), nullable=False)
    proposed_entry: Mapped[Decimal] = mapped_column(Numeric(12, 5), nullable=False)
    proposed_stop: Mapped[Decimal] = mapped_column(Numeric(12, 5), nullable=False)
    proposed_tp1: Mapped[Decimal | None] = mapped_column(Numeric(12, 5), nullable=True)
    lot_size: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    risk_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    expected_rr: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    policy_check_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    safety_check_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
