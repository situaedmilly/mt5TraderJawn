
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text

from app.db.base import Base


class ManualTradeJournal(Base):
    __tablename__ = "manual_trade_journal"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("signals.id"), index=True)
    taken: Mapped[bool] = mapped_column(Boolean, default=False)
    mt5_ticket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    actual_entry: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    actual_stop: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    actual_target: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    lot_size: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    risk_percent: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True)
    result_status: Mapped[str] = mapped_column(String(16), default="open")
    pnl_amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
