from datetime import datetime, timedelta, timezone


def scan_xauusd_reclaim(strategy_id: str, symbol_id: str) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "strategy_id": strategy_id,
        "symbol_id": symbol_id,
        "signal_time": now,
        "session_name": "new_york",
        "direction": "long",
        "status": "new",
        "priority_score": 8.4,
        "confidence_band": "A",
        "htf_bias": "bullish",
        "entry_tf": "M5",
        "entry_zone_low": 3032.10,
        "entry_zone_high": 3032.60,
        "stop_price": 3029.90,
        "target_1": 3036.80,
        "target_2": 3040.20,
        "expiry_time": now + timedelta(minutes=10),
        "reason_code": "ny_sweep_reclaim",
        "reason_text": "Sweep below local low, reclaim above trigger shelf, H1 aligned.",
        "json_context": {"spread_ok": True, "liquidity_sweep": True},
    }
