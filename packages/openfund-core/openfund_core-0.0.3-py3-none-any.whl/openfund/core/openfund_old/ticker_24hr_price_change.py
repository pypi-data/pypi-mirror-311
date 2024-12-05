#!/usr/bin/env python
import csv
import time
import os
import sys
import schedule


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from datetime import datetime
from binance.um_futures import UMFutures
from binance.error import ClientError
from libs.time_tools import format_timestamp, format_date, format_date_to
from libs.file_tools import create_path
from libs.prepare_env import get_api_key, get_path
from libs import enums
from libs.log_tools import Logger


data_path, log_path = get_path()
um_futures_client = UMFutures()


# 暂停秒数
sleepSec = 5

app = "ticker_24hr_price_change"
logger = Logger(app).get_log()
# fileName = "{}/{}_{}.log".format(
#     log_path, app, format_timestamp(datetime.now().timestamp() * 1000)
# )
# logging.basicConfig(
#     format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.INFO,
#     filename=fileName,
# )


def job():
    records = 0  # 累计记录数
    logger.info("{} app 开始 ++++++++++++++++++++++++++++ ".format(app))
    listData = []

    try:
        listData = um_futures_client.ticker_24hr_price_change()
    except Exception as e:
        print("Error:", e)
        logger.error(e)

    latestRecords = len(listData)
    path = "{}/{}/".format(data_path, app)
    create_path(path)  # 不存在路径进行呢创建
    with open(
        "{}{}_{}.csv".format(
            path,
            app,
            format_date(datetime.now().timestamp() * 1000),
        ),
        "a",
        newline="",
    ) as file:
        fieldnames = [
            "symbol",
            "priceChange",
            "priceChangePercent",
            "weightedAvgPrice",
            "lastPrice",
            "lastQty",
            "openPrice",
            "highPrice",
            "lowPrice",
            "volume",
            "quoteVolume",
            "openTime",
            "closeTime",
            "firstId",
            "lastId",
            "count",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(listData, key=lambda x: x["symbol"]):
            writer.writerow(row)

        logger.info("2、{}条写入文件...".format(latestRecords))

    logger.info("{} app 结束 --------------------------------- ".format(app))


if __name__ == "__main__":
    schedule.every(sleepSec).seconds.do(job)
    logger.info("Schedule Starting {0}sec ...... ".format(sleepSec))
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
