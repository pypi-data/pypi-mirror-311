from __future__ import annotations


import logging
import time
from pathlib import Path

from openfund.core.api_tools.enums import KlineInterval
from openfund.core.base_tool import Tool as BaseTool
from openfund.core.api_tools.binance_futures_tools import BinanceUMFuturesTool
from openfund.core.base_collector import Collector as BaseCollector

from openfund.core.utils.time_tools import TimeTools

logger = logging.getLogger(__name__)


class KLinesCollector(BaseCollector):
    def __init__(
        self,
        hisSwitch: int = 0,
        hisDateTime: int = 0,
        pool: list = None,
        interval: int = 5,
        client: BaseTool = None,
    ) -> None:
        super().__init__()
        self._pool = pool
        if self._pool is None:
            self._pool = ["BTCUSDT", "ETHUSDT"]
        logger.debug("+++++++++++++++ KLinesCollector init +++++++++++++ ")

        self._interval = interval
        self._hisSwitch = hisSwitch
        self._hisDateTime = hisDateTime
        self._dataDir = self.openfund.dataDir
        self._client = client
        if self._client is None:
            self._client = BinanceUMFuturesTool().umclient
        # self._job = None

    def collect(self) -> None:

        for symbol in self._pool:
            logger.debug("{} symbol 开始 ++++++++++++++++++++++++++++ ".format(symbol))
            latestRecords = 1  # 采集最近一次的记录数量
            records = 0  # 累计记录数
            queryCount = 0  # 执行次数
            nextEndTime = 0
            params = {"limit": 1000}
            while latestRecords != 0:  # 循环读取，直到记录为空
                queryCount += 1
                if nextEndTime != 0:
                    params = {"limit": 1000, "endTime": nextEndTime}

                logger.debug("1、{}第{}次开始执行...".format(symbol, queryCount))
                listData = []
                try:
                    listData = self._client.klines(
                        symbol,
                        KlineInterval.getByUnit(self._interval, "m"),
                        **params,
                    )
                except Exception as e:
                    # print("Error:", e)
                    logger.error(e)
                    time.sleep(10)
                    continue

                latestRecords = len(listData)
                data_file = Path(
                    self._dataDir.joinpath("klines")
                    .joinpath(symbol)
                    .joinpath(
                        "klines_{}.csv".format(
                            KlineInterval.getByUnit(self._interval, "m")
                        )
                    )
                )
                self._write_to_csv(data_file, listData)

                if latestRecords > 0:
                    nextEndTime = (
                        # -1 不和close时间戳相同,避免重新拉取重复数据
                        listData[0][0]
                        - 1
                    )

                    logger.debug(
                        "3、下次结束时间 %s %s"
                        % (TimeTools.format_timestamp(nextEndTime), nextEndTime)
                    )

                    if self._hisSwitch == 0 or nextEndTime <= self._hisDateTime:
                        break
                else:
                    logger.debug("4、结束...")

                # time.sleep(0.1)
            records = latestRecords + records
            logger.info("5、{} 抓取数据 {} 条记录...".format(symbol, records))
            logger.debug("{} symbol --------------------------------- ".format(symbol))

    # def taskDetail(taskName: str):
    #     currTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     logger.debug(f"{taskName}-->", "currTime:", currTime)

    def start(self) -> int:

        # self.collect()
        self._job = self.openfund.scheduler.add_job(
            func=self.collect,
            trigger="interval",
            # minutes=self._interval,
            seconds=self._interval,
            id="um_futures_collector",
        )

        logger.debug("调度任务已启动,每%s分钟执行一次。", self._interval)

        return 0


# if __name__ == "__main__":
#     from openfund.core.services.um_futures_collector import KLinesCollector

#     collector = KLinesCollector()

#     collector.start()
#     logger.debug(f"main   collector.start()  ===== ")
#     i = 0
#     while i < 10:

#         logger.debug("main i=%s ===== ", i)
#         if i == 2:
#             collector.pause()
#         if i == 4:
#             collector.resume()
#         if i == 8:
#             collector.stop()
#         time.sleep(5)
#         i += 1
