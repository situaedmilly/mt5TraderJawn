from app.core.db import engine, SessionLocal
from app.db.base import Base
from app.db.models import Strategy, Symbol


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Symbol).filter(Symbol.symbol == "XAUUSD").first():
            db.add(Symbol(symbol="XAUUSD", display_name="Gold Spot", asset_class="metal"))
        if not db.query(Symbol).filter(Symbol.symbol == "EURUSD").first():
            db.add(Symbol(symbol="EURUSD", display_name="Euro vs US Dollar", asset_class="fx"))

        if not db.query(Strategy).filter(Strategy.code == "ny_sweep_reclaim").first():
            db.add(
                Strategy(
                    name="NY Sweep Reclaim",
                    code="ny_sweep_reclaim",
                    description="Sweep liquidity and reclaim with H1 alignment",
                    phase="phase1",
                    timeframe_bias="H1",
                    timeframe_entry="M5",
                )
            )

        db.commit()
        print("Seed complete")
    finally:
        db.close()


if __name__ == "__main__":
    main()
