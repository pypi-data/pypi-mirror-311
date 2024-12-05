#!/usr/bin/env python
import csv
import time
import os
import sys
import json
import schedule

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from datetime import datetime
from binance.um_futures import UMFutures
from binance.error import ClientError
from utils.time_tools import format_timestamp, format_date, format_date_to
from utils.file_tools import create_path
from utils.prepare_env import get_api_key, get_path
from utils import enums
from utils.log_tools import Logger

data_path, log_path = get_path()
um_futures_client = UMFutures()

# 下次执行周期 5min
nextTimeMin = 5

app = "index_info"
logger = Logger(app).get_log()


def job():
    logger.info("{} app 开始 ++++++++++++++++++++++++++++ ".format(app))
    listData = []
    try:
        listData = um_futures_client.index_info()
    except Exception as e:
        print("Error:", e)
        logger.error(e)

    latestRecords = len(listData)

    path = "{}/{}/".format(data_path, app)
    create_path(path)  # 不存在路径进行呢创建

    with open(
        "{}{}_{}.txt".format(
            path,
            app,
            format_date(datetime.now().timestamp() * 1000),
        ),
        "a",
    ) as file:
        file.writelines(
            json.dumps(sorted(listData, key=lambda x: x["symbol"])) + "\r\n"
        )

    logger.info("1、本次 {} 抓取数据 {} 条记录...".format(app, records))
    logger.info("{} app --------------------------------- ".format(app))


if __name__ == "__main__":
    schedule.every(nextTimeMin).minutes.do(job)
    logger.info("Schedule Starting {0}min ...... ".format(nextTimeMin))
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
