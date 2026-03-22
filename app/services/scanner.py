from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
def scan_xauusd_reclaim(strategy_id: UUID, symbol_id: UUID) -> dict:
    """
    Stub scanner for XAUUSD reclaim strategy

    In production, this would:
    - Fetch price data from MT5 or data provider
    - Apply strategy rules
    - Calculate entry/stop/target levels
    - Return structured signal data

    Returns:
        dict: Signal data matching SignalCreate schema
    """
    return {
        "strategy_id": strategy_id,
        "symbol_id": symbol_id,
        "signal_time": datetime.now(timezone.utc),
        "direction": "long",
        "session_name": "london",
        "priority_score": 85.5,
        "confidence_band": "high",
        "htf_bias": "bullish",
        "entry_tf": "M15",
        "entry_zone_low": Decimal("2018.50"),
        "entry_zone_high": Decimal("2020.00"),
        "stop_price": Decimal("2015.00"),
        "target_1": Decimal("2028.00"),
        "target_2": Decimal("2035.00"),
        "expiry_time": None,
        "reason_code": "RECLAIM_AFTER_SWEEP",
        "reason_text": "HTF bullish, LTF swept liquidity and reclaimed structure",
        "json_context": {
            "swept_low": 2016.20,
            "structure_level": 2019.00,
            "volume_confirmation": True,
        },
    }
def scan_eurusd_fvg_fill(strategy_id: UUID, symbol_id: UUID) -> dict:
    """
    Stub scanner for EURUSD FVG fill strategy

    Returns:
        dict: Signal data matching SignalCreate schema
    """
    return {
        "strategy_id": strategy_id,
        "symbol_id": symbol_id,
        "signal_time": datetime.now(timezone.utc),
        "direction": "short",
        "session_name": "newyork",
        "priority_score": 78.0,
        "confidence_band": "medium",
        "htf_bias": "bearish",
        "entry_tf": "M5",
        "entry_zone_low": Decimal("1.0825"),
        "entry_zone_high": Decimal("1.0832"),
        "stop_price": Decimal("1.0845"),
        "target_1": Decimal("1.0795"),
        "target_2": Decimal("1.0780"),
        "expiry_time": None,
        "reason_code": "FVG_FILL",
        "reason_text": "HTF bearish, price filling FVG at premium level",
        "json_context": {
            "fvg_top": 1.0832,
            "fvg_bottom": 1.0825,
            "discount_array": [1.0795, 1.0780, 1.0765],
        },
    }
