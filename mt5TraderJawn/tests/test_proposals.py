from datetime import datetime, timedelta, timezone


def seed_signal(client):
    from app.api.deps import get_db
    from app.main import app
    from app.db.models.signal import Signal
    from app.db.models.strategy import Strategy
    from app.db.models.symbol import Symbol

    gen = app.dependency_overrides[get_db]()
    db = next(gen)
    symbol = Symbol(symbol="EURUSD", display_name="Euro Dollar", asset_class="fx")
    strategy = Strategy(
        name="London Breakout",
        code="london_breakout",
        description="test",
        phase="phase2",
        timeframe_bias="H1",
        timeframe_entry="M5",
    )
    db.add(symbol)
    db.add(strategy)
    db.commit()
    db.refresh(symbol)
    db.refresh(strategy)

    signal = Signal(
        strategy_id=strategy.id,
        symbol_id=symbol.id,
        signal_time=datetime.now(timezone.utc),
        session_name="london",
        direction="long",
        status="new",
        priority_score=7.5,
        confidence_band="A",
        htf_bias="bullish",
        entry_tf="M5",
        entry_zone_low=1.08,
        entry_zone_high=1.081,
        stop_price=1.079,
        target_1=1.084,
        target_2=None,
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=15),
        reason_code="london_breakout",
        reason_text="test",
        json_context={"spread_ok": True},
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    db.close()
    return signal.id


def test_create_and_review_proposal(client):
    signal_id = seed_signal(client)
    now = datetime.now(timezone.utc)
    payload = {
        "signal_id": str(signal_id),
        "order_type": "market",
        "proposed_entry": 1.081,
        "proposed_stop": 1.079,
        "proposed_tp1": 1.084,
        "lot_size": 0.1,
        "risk_percent": 0.5,
        "expected_rr": 1.5,
        "expires_at": (now + timedelta(minutes=15)).isoformat(),
        "policy_check_passed": True,
        "safety_check_passed": True,
    }

    create_response = client.post("/proposals", json=payload)
    assert create_response.status_code == 200
    proposal_id = create_response.json()["id"]

    review_response = client.post(f"/proposals/{proposal_id}/review", json={"decision": "approved"})
    assert review_response.status_code == 200
    assert review_response.json()["decision"] == "approved"
