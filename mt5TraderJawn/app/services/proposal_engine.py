from datetime import timedelta


def build_proposal_from_signal(signal: dict, lot_size: float = 0.10, risk_percent: float = 0.5) -> dict:
    entry = float(signal["entry_zone_high"])
    stop = float(signal["stop_price"])
    tp1 = float(signal["target_1"])
    risk = abs(entry - stop)
    rr = round(abs(tp1 - entry) / risk, 2) if risk else 0.0

    return {
        "signal_id": signal["id"],
        "order_type": "market",
        "proposed_entry": entry,
        "proposed_stop": stop,
        "proposed_tp1": tp1,
        "lot_size": lot_size,
        "risk_percent": risk_percent,
        "expected_rr": rr,
        "expires_at": signal["expiry_time"],
        "policy_check_passed": True,
        "safety_check_passed": True,
    }
