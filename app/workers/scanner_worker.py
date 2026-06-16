"""
Scanner worker
Runs periodically to scan markets and generate signals.
Can be run as a cron job or background service, or invoked on demand
for a single symbol, e.g.:

    python -m app.workers.scanner_worker --symbol SPY
"""
import argparse
import logging

from sqlalchemy import select

from app.core.db import SessionLocal
from app.db.models.strategy import Strategy
from app.db.models.symbol import Symbol
from app.db.models.signal import Signal
from app.services.mt5_client import MT5BridgeError
from app.services.scanner import scan_eurusd_fvg_fill, scan_spy, scan_xauusd_reclaim

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Maps a symbol code to the strategy code and scan function that apply to it
SYMBOL_SCANNERS = {
    "XAUUSD": ("XAUUSD_RECLAIM", scan_xauusd_reclaim),
    "EURUSD": ("EURUSD_FVG", scan_eurusd_fvg_fill),
    "SPY": ("SPY_ORB", scan_spy),
}


def _run_symbol_scan(db, symbol: Symbol, strategy: Strategy, scan_fn) -> Signal | None:
    logger.info(f"Scanning {symbol.symbol} with strategy {strategy.code}")
    try:
        signal_data = scan_fn(strategy.id, symbol.id)
    except MT5BridgeError as e:
        logger.error(f"MT5 bridge unavailable while scanning {symbol.symbol}: {e}")
        return None
    if not signal_data:
        logger.info(f"No setup found for {symbol.symbol}")
        return None
    signal = Signal(**signal_data)
    db.add(signal)
    db.commit()
    logger.info(f"Created signal {signal.id} for {symbol.symbol} - {signal.direction}")
    return signal


def run_scanner(symbol_code: str | None = None):
    """
    Execute market scanning workflow

    Args:
        symbol_code: if given, only scan this symbol (e.g. "SPY").
                     Otherwise scan every active symbol that has a
                     known scanner and an active matching strategy.
    """
    logger.info("Starting scanner worker run")
    db = SessionLocal()
    try:
        targets = [symbol_code] if symbol_code else list(SYMBOL_SCANNERS.keys())
        for code in targets:
            if code not in SYMBOL_SCANNERS:
                logger.warning(f"No scanner registered for symbol {code}")
                continue
            strategy_code, scan_fn = SYMBOL_SCANNERS[code]
            symbol = db.scalars(
                select(Symbol).where(Symbol.symbol == code, Symbol.is_active == True)
            ).first()
            if not symbol:
                logger.warning(f"Active symbol not found: {code}")
                continue
            strategy = db.scalars(
                select(Strategy).where(Strategy.code == strategy_code, Strategy.is_active == True)
            ).first()
            if not strategy:
                logger.warning(f"Active strategy not found: {strategy_code}")
                continue
            _run_symbol_scan(db, symbol, strategy, scan_fn)
    except Exception as e:
        logger.error(f"Scanner error: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
    logger.info("Scanner worker run completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the market scanner")
    parser.add_argument(
        "--symbol",
        help="Only scan this symbol (e.g. SPY). Omit to scan all known symbols.",
    )
    args = parser.parse_args()
    run_scanner(symbol_code=args.symbol)
