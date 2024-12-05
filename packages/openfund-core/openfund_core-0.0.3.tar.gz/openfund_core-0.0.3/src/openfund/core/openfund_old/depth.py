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
from libs.time_tools import format_timestamp, format_date
from libs.file_tools import create_path
from libs.prepare_env import get_api_key, get_path
from libs import enums
from libs.log_tools import Logger

data_path, log_path = get_path()

um_futures_client = UMFutures()

POOL = enums.NEW_SYMBOL_POLL
interval = enums.KLINE_INTERVAL_5MINUTE
# 历史截止数据开关
hisSwitch = 0
# hisSwitch 打开的情况下，抓取数据截止时间
hisDateTime = 1653974399999
# 发现异常后累计失败次数上限，超过后退出。
errorLimit = 100
# 异常后暂停秒数
sleepSec = 10
# 下次执行周期 5min
nextTimeMin = 5

app = "depth"
logger = Logger(app).get_log()


# logging.basicConfig(
#     format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.INFO,
#     filename="{}/{}_{}.log".format(
#         log_path, app, format_timestamp(datetime.now().timestamp() * 1000)
#     ),
# )
def job():
    logger.info("{} app 开始 ++++++++++++++++++++++++++++ ".format(app))
    latestRecords = 1
    params = {"limit": 1000}
    for symbol in POOL:
        queryTimes = queryTimes + 1
        logger.info("1、{}第{}次开始执行...".format(symbol, queryTimes))
        listData = []
        try:
            listData = um_futures_client.depth(symbol, **params)
        except Exception as e:
            logger.error(e)
            time.sleep(sleepSec)
            continue

        latestRecords = len(listData)
        records = latestRecords + records
        logger.info("2、{}条写入文件...".format(latestRecords))

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
            file.writelines(json.dumps(listData) + "\r\n")

    logger.info("3、本次 {} 抓取数据 {} 条记录...".format(app, records))
    logger.info("{} app --------------------------------- ".format(app))


if __name__ == "__main__":
    schedule.every(nextTimeMin).minutes.do(job)
    logger.info("Schedule Starting {0}min ...... ".format(nextTimeMin))
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
