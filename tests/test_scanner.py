"""SPY opening range breakout scanner tests"""
from uuid import uuid4

import pytest

from app.services.mt5_client import MT5BridgeError, MT5Client
from app.services.scanner import OPENING_RANGE_BARS, scan_spy


class FakeBridge:
    """Stand-in for MT5Client that returns canned bars"""

    def __init__(self, bars):
        self.bars = bars

    def fetch_bars(self, symbol, timeframe, start, count):
        return self.bars


def _bar(high, low, close):
    return {"time": "2026-06-16T13:30:00Z", "open": low, "high": high, "low": low, "close": close, "volume": 1000}


def _opening_range_bars():
    # First OPENING_RANGE_BARS bars define a 100.00 - 101.00 range
    return [_bar(101.0, 100.0, 100.5) for _ in range(OPENING_RANGE_BARS)]


def test_scan_spy_long_breakout():
    bars = _opening_range_bars() + [_bar(101.6, 101.2, 101.5)]
    client = FakeBridge(bars)
    result = scan_spy(uuid4(), uuid4(), client=client)
    assert result is not None
    assert result["direction"] == "long"
    assert result["reason_code"] == "ORB_BREAKOUT_LONG"
    assert float(result["stop_price"]) == 100.0


def test_scan_spy_short_breakout():
    bars = _opening_range_bars() + [_bar(99.8, 99.2, 99.5)]
    client = FakeBridge(bars)
    result = scan_spy(uuid4(), uuid4(), client=client)
    assert result is not None
    assert result["direction"] == "short"
    assert result["reason_code"] == "ORB_BREAKOUT_SHORT"
    assert float(result["stop_price"]) == 101.0


def test_scan_spy_no_breakout():
    bars = _opening_range_bars() + [_bar(100.8, 100.2, 100.6)]
    client = FakeBridge(bars)
    result = scan_spy(uuid4(), uuid4(), client=client)
    assert result is None


def test_scan_spy_insufficient_bars():
    client = FakeBridge(_opening_range_bars()[:2])
    result = scan_spy(uuid4(), uuid4(), client=client)
    assert result is None


def test_mt5_client_requires_host_and_port():
    with pytest.raises(MT5BridgeError):
        MT5Client(host=None, port=None)
