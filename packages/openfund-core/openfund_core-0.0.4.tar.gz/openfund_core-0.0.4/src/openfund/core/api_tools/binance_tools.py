from __future__ import annotations

import logging
from poetry.utils.authenticator import Authenticator

from typing import TYPE_CHECKING

from openfund.core.base_tool import Tool as BaseTool
from openfund.core.pyopenfund import Openfund


logger = logging.getLogger(__name__)


class BinanceTools(BaseTool):
    def __init__(self, openfund: Openfund | None = None) -> None:
        super().__init__(openfund, "binance")

    def get_time(self):
        return self.client.time()

    def get_account(self):
        return self.client.account()

    def get_klines(self, symbol: str, interval: str, **kwargs):
        return self.client.klines(symbol=symbol, interval=interval, **kwargs)
