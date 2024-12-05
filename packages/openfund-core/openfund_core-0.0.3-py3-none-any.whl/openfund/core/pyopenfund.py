from __future__ import annotations

import logging
import os
import sys

from typing import TYPE_CHECKING

from pathlib import Path

from platformdirs import user_cache_path
from platformdirs import user_config_path
from platformdirs import user_data_path
from platformdirs import user_log_path
from apscheduler.schedulers.background import BackgroundScheduler

if TYPE_CHECKING:
    from poetry.poetry import Poetry
    from openfund.core.factory import Factory

logger = logging.getLogger(__name__)
_APP_NAME = "pyopenfund"


class Openfund:
    def __init__(self, poetry: Openfund) -> None:
        self._poetry: Poetry = poetry
        self._schedule: BackgroundScheduler = None

    @property
    def poetry(self) -> Poetry:
        from pathlib import Path

        if self._poetry is not None:
            return self._poetry

        project_path = Path.cwd()

        self._poetry = Factory().create_poetry(
            cwd=project_path,
        )

        return self._poetry

    @property
    def dataDir(self) -> Path:
        # openfund_home = os.getenv("OPENFUND_HOME")
        # if openfund_home:
        #     return Path(openfund_home).expanduser()
        return Path(
            os.getenv("OPENFUND_DATA_DIR")
            or user_data_path(_APP_NAME, appauthor=False, roaming=True)
        ).joinpath("data")

    @property
    def cacheDir(self) -> Path:
        return Path(
            os.getenv("OPENFUND_CACHE_DIR")
            or user_cache_path(_APP_NAME, appauthor=False)
        )

    @property
    def configDir(self) -> Path:

        return Path(
            os.getenv("OPENFUND_CONFIG_DIR")
            or user_config_path(_APP_NAME, appauthor=False, roaming=True)
        ).joinpath("config")

    @property
    def logDir(self) -> Path:

        return Path(
            os.getenv("OPENFUND_LOG_DIR")
            or user_log_path(_APP_NAME, appauthor=False, roaming=True)
        )

    @property
    def scheduler(self) -> BackgroundScheduler:
        if self._schedule is None:
            self._schedule = BackgroundScheduler(
                timezone="MST",
            )

        return self._schedule
