from __future__ import annotations

import logging
import requests

from typing import TYPE_CHECKING

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from openfund.core.services.um_futures_collector import KLinesCollector

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from openfund.core.pyopenfund import Openfund

logger = logging.getLogger(__name__)


def test_um_KLinesCollector(openfund: Openfund, mocker: MockerFixture) -> None:
    logger.debug("------------ test_um_KLinesCollector ... -------------")

    try:
        KLinesCollector().start()
    except Exception as e:
        logger.error(e)
    # finally:
