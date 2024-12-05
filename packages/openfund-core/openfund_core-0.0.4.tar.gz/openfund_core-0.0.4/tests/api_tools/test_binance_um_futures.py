from __future__ import annotations

import os
import logging
import requests

from pathlib import Path
from typing import TYPE_CHECKING

from openfund.core.factory import Factory
from openfund.core.api_tools.binance_futures_tools import BinanceUMFuturesTools

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from openfund.core.pyopenfund import Openfund

logger = logging.getLogger(__name__)


def test_um_ping(openfund: Openfund, mocker: MockerFixture) -> None:
    logger.debug("------------ test_um_ping ... -------------")

    resp = None
    try:
        resp = BinanceUMFuturesTools(openfund).ping()
    except (requests.ConnectionError, requests.HTTPError) as e:
        raise HTTPError(e)

    logger.debug("------------ resp=%s ", resp)
    assert resp != None


def test_um_time(openfund: Openfund, mocker: MockerFixture) -> None:
    logger.debug("------------ test_um_time ... -------------")

    resp = None
    try:
        resp = BinanceUMFuturesTools(openfund).time()
    except (requests.ConnectionError, requests.HTTPError) as e:
        raise HTTPError(e)
    # finally:

    logger.debug("------------ resp=%s ", resp)
    assert resp != None


def test_um_klines(openfund: Openfund, mocker: MockerFixture) -> None:
    logger.debug("------------ test_um_klines ... -------------")

    resp = None
    try:
        resp = BinanceUMFuturesTools(openfund).klines("BTCUSDT")
    except (requests.ConnectionError, requests.HTTPError) as e:
        raise HTTPError(e)
    # finally:

    logger.debug("------------ resp=%s ", resp)
    assert resp != None
