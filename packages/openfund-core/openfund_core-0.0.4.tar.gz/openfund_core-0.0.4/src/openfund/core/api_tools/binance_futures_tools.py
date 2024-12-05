from __future__ import annotations

import logging

from openfund.core.base_tool import Tool as BaseTool
from openfund.core.pyopenfund import Openfund


logger = logging.getLogger(__name__)


class BinanceUMFuturesTool(BaseTool):
    def __init__(self, openfund: Openfund | None = None) -> None:
        super().__init__(openfund, "binance")

    def time(self):
        return self.umclient.time()

    def ping(self):
        return self.umclient.ping()

    def klines(self, symbol: str, interval: str = "1m", **kwargs):
        return self.umclient.klines(symbol=symbol, interval=interval, **kwargs)
