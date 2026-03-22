from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class Heartbeat(Base):
    """Service health heartbeat"""
    __tablename__ = "heartbeats"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    service_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    instance_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    json_metrics: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
