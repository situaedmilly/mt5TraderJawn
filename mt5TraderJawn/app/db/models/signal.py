
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("strategies.id"))
    symbol_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("symbols.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    signal_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    session_name: Mapped[str] = mapped_column(String(32))
    direction: Mapped[str] = mapped_column(String(8))
    status: Mapped[str] = mapped_column(String(32), default="new", index=True)
    priority_score: Mapped[float] = mapped_column(Numeric(8, 2), default=0)
    confidence_band: Mapped[str] = mapped_column(String(4), default="B")
    htf_bias: Mapped[str] = mapped_column(String(16))
    entry_tf: Mapped[str] = mapped_column(String(16))
    entry_zone_low: Mapped[float] = mapped_column(Numeric(18, 6))
    entry_zone_high: Mapped[float] = mapped_column(Numeric(18, 6))
    stop_price: Mapped[float] = mapped_column(Numeric(18, 6))
    target_1: Mapped[float] = mapped_column(Numeric(18, 6))
    target_2: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    expiry_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason_code: Mapped[str] = mapped_column(String(64))
    reason_text: Mapped[str] = mapped_column(Text)
    json_context: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), default=dict)

    strategy = relationship("Strategy")
    symbol = relationship("Symbol")
