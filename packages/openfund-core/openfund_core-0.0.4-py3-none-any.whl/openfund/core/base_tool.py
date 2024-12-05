from __future__ import annotations

import logging

from pathlib import Path

from typing import TYPE_CHECKING

from poetry.utils.authenticator import Authenticator
from binance.spot import Spot as Client
from binance.um_futures import UMFutures as UMClient

from openfund.core.pyopenfund import Openfund
from openfund.core.factory import Factory


logger = logging.getLogger(__name__)


class Tool:
    def __init__(
        self, openfund: Openfund | None = None, toolname: str = "binance"
    ) -> None:
        self._openfund: Openfund = openfund
        if self._openfund is None:
            self._openfund = Factory.create_openfund()

        self._toolname = toolname
        self._password_manager = Authenticator(
            self._openfund._poetry.config
        )._password_manager

        self._client = None
        self._umclient = None

    @property
    def api_key(self) -> str:
        return self._password_manager.get_http_auth(self._toolname).get("username")

    @property
    def apk_secret(self) -> str:
        return self._password_manager.get_http_auth(self._toolname).get("password")

    @property
    def openfund(self) -> Openfund:
        return self._openfund

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(self.api_key, self.apk_secret)
        return self._client

    @property
    def umclient(self) -> UMClient:
        if self._umclient is None:
            self._umclient = UMClient(self.api_key, self.apk_secret)
        return self._umclient
