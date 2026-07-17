"""
Seed core reference data
Run this after initial migration to populate:
- Symbols
- Strategies
"""
import logging
from datetime import datetime, timezone
from app.core.db import SessionLocal
from app.db.models.symbol import Symbol
from app.db.models.strategy import Strategy
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def seed_symbols(db):
    """Seed trading symbols"""
    symbols_data = [
        {
            "symbol": "XAUUSD",
            "display_name": "Gold vs US Dollar",
            "asset_class": "metals",
        },
        {
            "symbol": "EURUSD",
            "display_name": "Euro vs US Dollar",
            "asset_class": "forex",
        },
        {
            "symbol": "GBPUSD",
            "display_name": "British Pound vs US Dollar",
            "asset_class": "forex",
        },
        {
            "symbol": "NAS100",
            "display_name": "NASDAQ 100 Index",
            "asset_class": "indices",
        },
        {
            "symbol": "SPY",
            "display_name": "SPDR S&P 500 ETF",
            "asset_class": "equities",
        },
    ]
    for data in symbols_data:
        existing = db.query(Symbol).filter(Symbol.symbol == data["symbol"]).first()
        if not existing:
            symbol = Symbol(**data)
            db.add(symbol)
            logger.info(f"Created symbol: {data['symbol']}")
        else:
            logger.info(f"Symbol already exists: {data['symbol']}")
    db.commit()
def seed_strategies(db):
    """Seed trading strategies"""
    strategies_data = [
        {
            "name": "Gold Reclaim Strategy",
            "code": "XAUUSD_RECLAIM",
            "description": "Reclaim structure after liquidity sweep on XAUUSD",
            "phase": "phase_1",
            "timeframe_bias": "H1",
            "timeframe_entry": "M15",
        },
        {
            "name": "EUR FVG Fill",
            "code": "EURUSD_FVG",
            "description": "Fair value gap fill strategy on EURUSD",
            "phase": "phase_1",
            "timeframe_bias": "H4",
            "timeframe_entry": "M5",
        },
        {
            "name": "GBP Orderblock",
            "code": "GBPUSD_OB",
            "description": "Order block entry on GBPUSD",
            "phase": "phase_1",
            "timeframe_bias": "H1",
            "timeframe_entry": "M15",
        },
        {
            "name": "SPY Opening Range Breakout",
            "code": "SPY_ORB",
            "description": "Breakout of the first 30 minutes' range on SPY",
            "phase": "phase_1",
            "timeframe_bias": "M5",
            "timeframe_entry": "M5",
        },
    ]
    for data in strategies_data:
        existing = db.query(Strategy).filter(Strategy.code == data["code"]).first()
        if not existing:
            strategy = Strategy(**data)
            db.add(strategy)
            logger.info(f"Created strategy: {data['code']}")
        else:
            logger.info(f"Strategy already exists: {data['code']}")
    db.commit()
def main():
    """Run all seed operations"""
    logger.info("Starting data seeding")
    db = SessionLocal()
    try:
        seed_symbols(db)
        seed_strategies(db)
        logger.info("Data seeding completed successfully")
    except Exception as e:
        logger.error(f"Seeding error: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
if __name__ == "__main__":
    main()
