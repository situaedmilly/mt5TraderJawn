"""
Scanner worker
Runs periodically to scan markets and generate signals.
Can be run as a cron job or background service.
"""
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from app.core.db import SessionLocal
from app.db.models.strategy import Strategy
from app.db.models.symbol import Symbol
from app.db.models.signal import Signal
from app.services.scanner import scan_xauusd_reclaim
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def run_scanner():
    """Execute market scanning workflow"""
    logger.info("Starting scanner worker run")
    db = SessionLocal()
    try:
        # Find active strategies
        stmt = select(Strategy).where(Strategy.is_active == True)
        strategies = db.scalars(stmt).all()
        if not strategies:
            logger.warning("No active strategies found")
            return
        # Find active symbols
        stmt = select(Symbol).where(Symbol.is_active == True)
        symbols = db.scalars(stmt).all()
        if not symbols:
            logger.warning("No active symbols found")
            return
        # For demo purposes, generate one stub signal
        # In production, would iterate through strategy-symbol combinations
        strategy = strategies[0]
        symbol = symbols[0]
        logger.info(f"Scanning {symbol.symbol} with strategy {strategy.code}")
        # Run scanner (stubbed)
        signal_data = scan_xauusd_reclaim(strategy.id, symbol.id)
        # Create signal
        signal = Signal(**signal_data)
        db.add(signal)
        db.commit()
        logger.info(f"Created signal {signal.id} for {symbol.symbol} - {signal.direction}")
    except Exception as e:
        logger.error(f"Scanner error: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
    logger.info("Scanner worker run completed")
if __name__ == "__main__":
    run_scanner()
