from datetime import datetime
from typing import Any


class MT5Client:
    """Placeholder interface for future MetaTrader 5 integration."""

    def connect(self, login: int, password: str, server: str) -> bool:
        raise NotImplementedError("MT5 connection not implemented")

    def disconnect(self) -> bool:
        raise NotImplementedError("MT5 disconnect not implemented")

    def fetch_bars(self, symbol: str, timeframe: str, start: datetime, count: int) -> list[dict[str, Any]]:
        raise NotImplementedError("MT5 bar fetch not implemented")

    def send_order(self, symbol: str, order_type: str, volume: float, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError("MT5 order send not implemented")

    def get_positions(self, symbol: str | None = None) -> list[dict[str, Any]]:
        raise NotImplementedError("MT5 position query not implemented")
