from __future__ import annotations

import logging
import csv

from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from apscheduler.job import Job

from openfund.core.pyopenfund import Openfund
from openfund.core.factory import Factory


logger = logging.getLogger(__name__)


class Collector:
    def __init__(self, openfund: Openfund | None = None) -> None:
        self._openfund: Openfund = openfund
        if self._openfund is None:
            self._openfund = Factory.create_openfund()
        self._job: Job = None

    @property
    def openfund(self) -> Openfund:
        return self._openfund

    @abstractmethod
    def collect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start(self) -> int:
        raise NotImplementedError()
        # from apscheduler.schedulers.background import BlockingScheduler

        # apSchedule = BlockingScheduler()
        # self.openfund.scheduler.add_job(
        #     func=self.collect, trigger="interval", minutes=5,seconds=5 id="um_futures_collector"
        # )

    def stop(self) -> int:
        if self._job is not None:
            self._job.remove()
        logger.debug(f"{self._job.name} is stop .")
        return 0

    def pause(self) -> int:
        if self._job is not None:
            self._job.pause()
        logger.debug(f"{self._job.name} is pause .")
        return 0

    def resume(self) -> int:
        if self._job is not None:
            self._job.resume()
        logger.debug(f"{self._job.name} is resume .")
        return 0

    def _write_to_csv(self, file: Path, listData: list) -> None:

        # 如果路径不存在，创建路径
        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "a", newline="") as file:
            writer = csv.writer(file)
            # 时间戳倒序，插入文件尾部
            writer.writerows(sorted(listData, key=lambda x: x[0], reverse=True))

        logger.debug("2、{}条写入{}文件...".format(len(listData), file))
