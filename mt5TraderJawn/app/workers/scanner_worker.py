from app.core.db import SessionLocal
from app.db.models.signal import Signal
from app.db.models.strategy import Strategy
from app.db.models.symbol import Symbol
from app.services.scanner import scan_xauusd_reclaim


def run_once() -> None:
    db = SessionLocal()
    try:
        strategy = db.query(Strategy).filter(Strategy.code == "ny_sweep_reclaim").first()
        symbol = db.query(Symbol).filter(Symbol.symbol == "XAUUSD").first()
        if not strategy or not symbol:
            raise RuntimeError("Seed core data first with scripts/seed_core_data.py")

        payload = scan_xauusd_reclaim(strategy_id=str(strategy.id), symbol_id=str(symbol.id))
        signal = Signal(**payload)
        db.add(signal)
        db.commit()
        print(f"Created signal {signal.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run_once()
