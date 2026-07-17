"""
MT5 bridge client

Talks to a lightweight HTTP bridge process that runs alongside the MT5
terminal (e.g. on the trading machine) and exposes REST endpoints for
market data and order management. This client never imports the
MetaTrader5 package directly -- it only speaks HTTP to the bridge, so it
works regardless of where the bridge process itself runs.

Expected bridge contract:
    POST /connect          {login, password, server}      -> {"connected": bool}
    POST /disconnect       {}                              -> {"disconnected": bool}
    GET  /bars              ?symbol&timeframe&start&count  -> [{"time","open","high","low","close","volume"}, ...]
    POST /orders            {symbol, order_type, volume,
                              price, stop_loss, take_profit,
                              comment}                      -> {"ticket": int, "status": str, ...}
    GET  /positions         ?symbol                        -> [{"ticket", "symbol", ...}, ...]
    GET  /account                                           -> {"balance", "equity", "margin", ...}
    POST /positions/{ticket}/modify {stop_loss, take_profit} -> {"success": bool}
    POST /positions/{ticket}/close                          -> {"success": bool}
"""
from datetime import datetime
from typing import Any, Dict, List

import httpx

from app.core.config import get_settings


class MT5BridgeError(Exception):
    """Raised when the MT5 bridge is unreachable or returns an error"""


class MT5Client:
    """
    HTTP client for the MT5 bridge service

    The bridge itself wraps the real MetaTrader5 terminal/Python package
    and runs wherever that terminal lives (e.g. the Mac/Windows machine
    running MT5). This client just calls it over the network.
    """

    def __init__(self, host: str, port: int, timeout: float = 10.0):
        if not host or not port:
            raise MT5BridgeError(
                "MT5 bridge host/port not configured (set MT5_HOST and MT5_PORT)"
            )
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout
        self.connected = False

    @classmethod
    def from_settings(cls) -> "MT5Client":
        """Build a client from app settings (.env MT5_HOST / MT5_PORT)"""
        settings = get_settings()
        return cls(host=settings.mt5_host, port=settings.mt5_port)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_url}{path}"
        try:
            response = httpx.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise MT5BridgeError(
                f"Bridge returned {exc.response.status_code} for {method} {path}: {exc.response.text}"
            ) from exc
        except httpx.RequestError as exc:
            raise MT5BridgeError(
                f"Could not reach MT5 bridge at {self.base_url} ({method} {path}): {exc}"
            ) from exc
        if response.content:
            return response.json()
        return None

    def connect(self, login: int, password: str, server: str) -> bool:
        """Establish connection to MT5 terminal via the bridge"""
        result = self._request(
            "POST",
            "/connect",
            json={"login": login, "password": password, "server": server},
        )
        self.connected = bool(result and result.get("connected"))
        return self.connected

    def disconnect(self) -> bool:
        """Close MT5 connection via the bridge"""
        result = self._request("POST", "/disconnect", json={})
        self.connected = False
        return bool(result and result.get("disconnected"))

    def fetch_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        count: int,
    ) -> List[Dict[str, Any]]:
        """Fetch historical OHLCV bars for a symbol from the bridge"""
        bars = self._request(
            "GET",
            "/bars",
            params={
                "symbol": symbol,
                "timeframe": timeframe,
                "start": start.isoformat(),
                "count": count,
            },
        )
        return bars or []

    def send_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: float = None,
        stop_loss: float = None,
        take_profit: float = None,
        comment: str = None,
    ) -> Dict[str, Any]:
        """Send a trade order via the bridge"""
        return self._request(
            "POST",
            "/orders",
            json={
                "symbol": symbol,
                "order_type": order_type,
                "volume": volume,
                "price": price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "comment": comment,
            },
        )

    def get_positions(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Query open positions via the bridge"""
        params = {"symbol": symbol} if symbol else None
        positions = self._request("GET", "/positions", params=params)
        return positions or []

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information via the bridge"""
        return self._request("GET", "/account")

    def modify_position(
        self,
        ticket: int,
        stop_loss: float = None,
        take_profit: float = None,
    ) -> bool:
        """Modify existing position SL/TP via the bridge"""
        result = self._request(
            "POST",
            f"/positions/{ticket}/modify",
            json={"stop_loss": stop_loss, "take_profit": take_profit},
        )
        return bool(result and result.get("success"))

    def close_position(self, ticket: int) -> bool:
        """Close an open position via the bridge"""
        result = self._request("POST", f"/positions/{ticket}/close", json={})
        return bool(result and result.get("success"))
