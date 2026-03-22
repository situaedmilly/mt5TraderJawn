from datetime import datetime, timedelta, timezone


def seed_symbol_and_strategy(client):
    from app.api.deps import get_db
    from app.main import app
    from app.db.models.strategy import Strategy
    from app.db.models.symbol import Symbol

    gen = app.dependency_overrides[get_db]()
    db = next(gen)
    symbol = Symbol(symbol="XAUUSD", display_name="Gold Spot", asset_class="metal")
    strategy = Strategy(
        name="NY Sweep Reclaim",
        code="ny_sweep_reclaim",
        description="test",
        phase="phase1",
        timeframe_bias="H1",
        timeframe_entry="M5",
    )
    db.add(symbol)
    db.add(strategy)
    db.commit()
    db.refresh(symbol)
    db.refresh(strategy)
    db.close()
    return symbol.id, strategy.id


def test_create_and_list_signal(client):
    symbol_id, strategy_id = seed_symbol_and_strategy(client)
    now = datetime.now(timezone.utc)

    payload = {
        "strategy_id": str(strategy_id),
        "symbol_id": str(symbol_id),
        "signal_time": now.isoformat(),
        "session_name": "new_york",
        "direction": "long",
        "status": "new",
        "priority_score": 8.4,
        "confidence_band": "A",
        "htf_bias": "bullish",
        "entry_tf": "M5",
        "entry_zone_low": 3032.1,
        "entry_zone_high": 3032.6,
        "stop_price": 3029.9,
        "target_1": 3036.8,
        "target_2": 3040.2,
        "expiry_time": (now + timedelta(minutes=10)).isoformat(),
        "reason_code": "ny_sweep_reclaim",
        "reason_text": "test signal",
        "json_context": {"spread_ok": True},
    }

    create_response = client.post("/signals", json=payload)
    assert create_response.status_code == 200
    body = create_response.json()
    assert body["session_name"] == "new_york"

    list_response = client.get("/signals")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1
