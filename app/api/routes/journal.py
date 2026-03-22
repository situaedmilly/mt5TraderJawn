from fastapi import APIRouter
from app.api.deps import DatabaseSession
from app.db.models.manual_trade_journal import ManualTradeJournal
from app.schemas.journal import JournalCreate, JournalResponse
router = APIRouter()
@router.post("", response_model=JournalResponse, status_code=201)
def create_journal_entry(journal_data: JournalCreate, db: DatabaseSession):
    """Create a manual trade journal entry"""
    journal = ManualTradeJournal(**journal_data.model_dump())
    db.add(journal)
    db.commit()
    db.refresh(journal)
    return journal
