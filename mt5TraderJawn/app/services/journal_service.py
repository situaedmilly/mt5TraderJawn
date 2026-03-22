from sqlalchemy.orm import Session

from app.db.models.manual_trade_journal import ManualTradeJournal
from app.schemas.journal import JournalCreate


def create_journal_entry(db: Session, payload: JournalCreate) -> ManualTradeJournal:
    row = ManualTradeJournal(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
