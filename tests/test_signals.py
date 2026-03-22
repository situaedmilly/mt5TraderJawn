"""Signal endpoint tests"""
from datetime import datetime, timezone
from decimal import Decimal
from app.db.models.symbol import Symbol
from app.db.models.strategy import Strategy
def test_create_signal(client, db_session):
    """Test signal creation"""
    # Create required dependencies
    symbol = Symbol(
        symbol="XAUUSD",
        display_name="Gold",
        asset_class="metals",
    )
    db_session.add(symbol)
    strategy = Strategy(
        name="Test Strategy",
        code="TEST_STRAT",
        phase="phase_1",
    )
    db_session.add(strategy)
    db_session.commit()
    # Create signal
    signal_data = {
        "strategy_id": str(strategy.id),
        "symbol_id": str(symbol.id),
        "signal_time": datetime.now(timezone.utc).isoformat(),
        "direction": "long",
        "entry_zone_low": "2000.00",
        "stop_price": "1990.00",
    }
    response = client.post("/signals", json=signal_data)
    assert response.status_code == 201
    data = response.json()
    assert data["direction"] == "long"
    assert data["status"] == "active"
def test_list_signals(client, db_session):
    """Test signal listing"""
    response = client.get("/signals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
