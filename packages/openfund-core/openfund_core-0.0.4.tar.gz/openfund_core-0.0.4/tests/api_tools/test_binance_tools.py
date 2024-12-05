from __future__ import annotations

import os
import logging
import requests

from pathlib import Path
from typing import TYPE_CHECKING

from openfund.core.factory import Factory
from openfund.core.api_tools.binance_tools import BinanceTools

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from openfund.core.pyopenfund import Openfund

logger = logging.getLogger(__name__)


def test_openfund(openfund: Openfund, mocker: MockerFixture) -> None:
    logger.debug("------------ test_openfund ... -------------")
    logger.debug(
        "------------ test_openfund cacheDir=%s ... -------------", openfund.cacheDir
    )
    logger.debug(
        "------------ test_openfund configDir=%s ... -------------", openfund.configDir
    )
    logger.debug(
        "------------ test_openfund dataDir=%s ... -------------", openfund.dataDir
    )


def test_binance_get_accont_by_env_config(
    openfund: Openfund, mocker: MockerFixture
) -> None:
    logger.debug("------------ test_binance_get_accont_by_default ... -------------")

    resp = None
    try:
        resp = BinanceTools(openfund).get_account()
    except (requests.ConnectionError, requests.HTTPError) as e:
        raise HTTPError(e)

    logger.debug("------------ resp=%s ", resp)
    assert resp != None
