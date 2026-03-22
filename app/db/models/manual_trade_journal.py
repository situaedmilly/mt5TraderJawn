from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class ManualTradeJournal(Base):
    """Manual trade journal entry for Phase 1 workflow"""
    __tablename__ = "manual_trade_journals"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    signal_id: Mapped[UUID] = mapped_column(ForeignKey("signals.id", ondelete="CASCADE"), index=True, nullable=False)
    taken: Mapped[bool] = mapped_column(Boolean, nullable=False)
    mt5_ticket: Mapped[str | None] = mapped_column(String(50), nullable=True)
    actual_entry: Mapped[Decimal | None] = mapped_column(Numeric(12, 5), nullable=True)
    actual_stop: Mapped[Decimal | None] = mapped_column(Numeric(12, 5), nullable=True)
    actual_target: Mapped[Decimal | None] = mapped_column(Numeric(12, 5), nullable=True)
    lot_size: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    risk_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    result_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pnl_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
