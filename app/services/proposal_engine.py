from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, Any
def signal_to_proposal(signal_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a signal into a trade proposal with risk calculations

    Args:
        signal_data: Dict containing signal fields

    Returns:
        dict: Proposal data matching ProposalCreate schema
    """
    direction = signal_data.get("direction")
    entry = signal_data.get("entry_zone_low") or signal_data.get("entry_zone_high")
    stop = signal_data.get("stop_price")
    target = signal_data.get("target_1")
    # Calculate risk-reward if data available
    expected_rr = None
    if entry and stop and target:
        risk = abs(float(entry) - float(stop))
        reward = abs(float(target) - float(entry))
        if risk > 0:
            expected_rr = Decimal(str(round(reward / risk, 2)))
    # Standard risk allocation
    risk_percent = Decimal("1.0")  # 1% risk per trade
    lot_size = Decimal("0.10")  # Base lot size (should be calculated from account size)
    # Order type based on entry zone
    order_type = "market"  # Could be "limit" or "stop" based on strategy
    # Expiry time (24 hours from now for limit orders)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    return {
        "signal_id": signal_data.get("id"),
        "order_type": order_type,
        "proposed_entry": entry,
        "proposed_stop": stop,
        "proposed_tp1": target,
        "lot_size": lot_size,
        "risk_percent": risk_percent,
        "expected_rr": expected_rr,
        "expires_at": expires_at,
    }
def calculate_position_size(
    account_balance: Decimal,
    risk_percent: Decimal,
    entry: Decimal,
    stop: Decimal,
    pip_value: Decimal,
) -> Decimal:
    """
    Calculate position size based on risk parameters

    Args:
        account_balance: Account equity
        risk_percent: Percentage of account to risk
        entry: Entry price
        stop: Stop loss price
        pip_value: Value per pip for instrument

    Returns:
        Decimal: Lot size
    """
    risk_amount = account_balance * (risk_percent / Decimal("100"))
    pips_at_risk = abs(entry - stop) * Decimal("10000")  # Assuming forex 4-digit
    lot_size = risk_amount / (pips_at_risk * pip_value)
    return round(lot_size, 2)
