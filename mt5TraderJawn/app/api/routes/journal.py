from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.manual_trade_journal import ManualTradeJournal
from app.schemas.journal import JournalCreate, JournalOut

router = APIRouter(prefix="/journal", tags=["journal"])


@router.post("", response_model=JournalOut)
def create_journal(payload: JournalCreate, db: Session = Depends(get_db)) -> ManualTradeJournal:
    row = ManualTradeJournal(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
