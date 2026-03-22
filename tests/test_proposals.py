"""Proposal endpoint tests"""
from datetime import datetime, timezone
from decimal import Decimal
from app.db.models.symbol import Symbol
from app.db.models.strategy import Strategy
from app.db.models.signal import Signal
def test_create_proposal(client, db_session):
    """Test proposal creation"""
    # Create dependencies
    symbol = Symbol(symbol="EURUSD", display_name="EUR/USD", asset_class="forex")
    db_session.add(symbol)
    strategy = Strategy(name="Test Strategy", code="TEST", phase="phase_2")
    db_session.add(strategy)
    db_session.commit()
    signal = Signal(
        strategy_id=strategy.id,
        symbol_id=symbol.id,
        signal_time=datetime.now(timezone.utc),
        direction="short",
    )
    db_session.add(signal)
    db_session.commit()
    # Create proposal
    proposal_data = {
        "signal_id": str(signal.id),
        "order_type": "market",
        "proposed_entry": "1.0850",
        "proposed_stop": "1.0870",
        "proposed_tp1": "1.0810",
        "lot_size": "0.10",
        "risk_percent": "1.0",
        "expected_rr": "2.0",
    }
    response = client.post("/proposals", json=proposal_data)
    assert response.status_code == 201
    data = response.json()
    assert data["proposal_status"] == "pending"
def test_review_proposal(client, db_session):
    """Test proposal review"""
    # Create dependencies
    symbol = Symbol(symbol="GBPUSD", display_name="GBP/USD", asset_class="forex")
    db_session.add(symbol)
    strategy = Strategy(name="Test Strategy", code="TEST2", phase="phase_2")
    db_session.add(strategy)
    db_session.commit()
    signal = Signal(
        strategy_id=strategy.id,
        symbol_id=symbol.id,
        signal_time=datetime.now(timezone.utc),
        direction="long",
    )
    db_session.add(signal)
    db_session.commit()
    # Create proposal first
    proposal_data = {
        "signal_id": str(signal.id),
        "order_type": "limit",
        "proposed_entry": "1.2500",
        "proposed_stop": "1.2480",
        "proposed_tp1": "1.2550",
        "lot_size": "0.10",
        "risk_percent": "1.0",
    }
    create_response = client.post("/proposals", json=proposal_data)
    proposal_id = create_response.json()["id"]
    # Review it
    review_data = {"decision": "approved", "review_note": "Good setup"}
    response = client.post(f"/proposals/{proposal_id}/review", json=review_data)
    assert response.status_code == 201
    data = response.json()
    assert data["decision"] == "approved"
