from datetime import datetime, time, timezone
from decimal import Decimal
from uuid import UUID

from app.services.mt5_client import MT5Client

OPENING_RANGE_BARS = 6  # 6 x M5 bars = first 30 minutes after open
MARKET_OPEN_UTC = time(13, 30)  # 9:30am ET


def scan_spy(strategy_id: UUID, symbol_id: UUID, client: MT5Client = None) -> dict | None:
    """
    Opening range breakout scanner for SPY

    Fetches the day's M5 bars from the MT5 bridge, builds the opening
    range from the first OPENING_RANGE_BARS bars after the open, and
    looks for a breakout on the most recently closed bar.

    Returns:
        dict matching SignalCreate, or None if no breakout setup is present
    """
    client = client or MT5Client.from_settings()
    today_open = datetime.now(timezone.utc).replace(
        hour=MARKET_OPEN_UTC.hour, minute=MARKET_OPEN_UTC.minute, second=0, microsecond=0
    )
    bars = client.fetch_bars(symbol="SPY", timeframe="M5", start=today_open, count=100)
    if len(bars) <= OPENING_RANGE_BARS:
        return None

    opening_range = bars[:OPENING_RANGE_BARS]
    or_high = max(Decimal(str(b["high"])) for b in opening_range)
    or_low = min(Decimal(str(b["low"])) for b in opening_range)
    or_range = or_high - or_low
    if or_range <= 0:
        return None

    last_bar = bars[-1]
    last_close = Decimal(str(last_bar["close"]))

    if last_close > or_high:
        direction = "long"
        entry_zone_low = or_high
        entry_zone_high = last_close
        stop_price = or_low
        target_1 = last_close + or_range
        target_2 = last_close + (or_range * 2)
        reason_code = "ORB_BREAKOUT_LONG"
        reason_text = "Price closed above the opening range high"
    elif last_close < or_low:
        direction = "short"
        entry_zone_low = last_close
        entry_zone_high = or_low
        stop_price = or_high
        target_1 = last_close - or_range
        target_2 = last_close - (or_range * 2)
        reason_code = "ORB_BREAKOUT_SHORT"
        reason_text = "Price closed below the opening range low"
    else:
        return None

    return {
        "strategy_id": strategy_id,
        "symbol_id": symbol_id,
        "signal_time": datetime.now(timezone.utc),
        "direction": direction,
        "session_name": "newyork",
        "priority_score": None,
        "confidence_band": None,
        "htf_bias": None,
        "entry_tf": "M5",
        "entry_zone_low": entry_zone_low,
        "entry_zone_high": entry_zone_high,
        "stop_price": stop_price,
        "target_1": target_1,
        "target_2": target_2,
        "expiry_time": None,
        "reason_code": reason_code,
        "reason_text": reason_text,
        "json_context": {
            "or_high": float(or_high),
            "or_low": float(or_low),
            "last_close": float(last_close),
            "bars_seen": len(bars),
        },
    }


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
