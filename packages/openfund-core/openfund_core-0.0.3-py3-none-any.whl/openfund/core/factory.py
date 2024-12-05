from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING

from poetry.factory import Factory as BaseFactory
from openfund.core.pyopenfund import Openfund


if TYPE_CHECKING:
    from poetry.poetry import Poetry


logger = logging.getLogger(__name__)
_APP_NAME = "pyopenfund"


class Factory(BaseFactory):
    _openfund: Openfund = None

    def __init__(self) -> None:
        super().__init__()
        self._init_log()

    def create_poetry(
        self,
        cwd: Path | None = None,
        with_groups: bool = True,
    ) -> Poetry:
        poetry = super().create_poetry(cwd=cwd, with_groups=with_groups)
        return poetry

    @classmethod
    def create_openfund(
        cls,
        cwd: Path | None = None,
        with_groups: bool = True,
    ) -> Openfund:
        if cls._openfund is not None:
            return cls._openfund

        if cwd is None:
            cwd = Path.cwd()

        poetry = Factory().create_poetry(cwd=cwd, with_groups=with_groups)
        cls._openfund = Openfund(poetry)
        cls._openfund.scheduler.start()
        return cls._openfund

    def _init_log(self):
        from openfund.core.pyopenfund import user_log_path

        log_file = user_log_path(
            _APP_NAME, appauthor=False, ensure_exists=True
        ).resolve()
        log_file = (
            user_log_path(_APP_NAME, appauthor=False, ensure_exists=True)
            .joinpath("openfund-core.log")
            .resolve()
        )
        fileHandler = FileHandler(log_file)
        fileHandler.setFormatter(FileFormatter())
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(FileFormatter())
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[console_handler, fileHandler],
        )


from logging.handlers import TimedRotatingFileHandler


class FileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding=None,
        delay=False,
        utc=False,
    ) -> None:
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)


class FileFormatter(logging.Formatter):

    _format = "%(asctime)s - %(process)d | %(threadName)s | %(module)s.%(funcName)s:%(lineno)d - %(levelname)s -%(message)s"

    _datefmt = "%Y-%m-%d-%H:%M:%S"  # 时间

    def __init__(self, fmt=_format, datefmt=_datefmt, style="%") -> None:
        super().__init__(fmt, datefmt, style)
