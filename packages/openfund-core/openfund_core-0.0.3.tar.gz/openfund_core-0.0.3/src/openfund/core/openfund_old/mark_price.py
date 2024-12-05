#!/usr/bin/env python
import csv
import time
import os
import sys
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from datetime import datetime
from binance.um_futures import UMFutures
from binance.error import ClientError
from libs.time_tools import format_timestamp, format_date, format_date_to
from libs.file_tools import create_path
from libs.prepare_env import get_path
from libs import enums
from libs.log_tools import Logger

data_path, log_path = get_path()
um_futures_client = UMFutures()


# 暂停秒数
sleepSec = 10
#
nextTimesSec = 0

app = "mark_price"
logger = Logger(app).get_log()
# fileName = "{}/{}_{}.log".format(
#     log_path, app, format_timestamp(datetime.now().timestamp() * 1000)
# )
# logger.basicConfig(
#     format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logger.INFO,
#     filename=fileName,
# )

latestRecords = 1
records = 0  # 累计记录数
queryTimes = 0  # 执行次数
errorCount = 0  # 异常次数
while True:
    queryTimes = queryTimes + 1
    logger.info("{} app 开始 ++++++++++++++++++++++++++++ ".format(app))
    logger.info("1、第{}次开始执行...".format(queryTimes))
    listData = []
    try:
        listData = um_futures_client.mark_price()
    except KeyError as err:
        print("KeyError:", err)
        logger.error(err)
        break
    except ClientError as error:
        logger.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
        if error.error_code == -4144 and error.status_code == 400:
            break
    except Exception as e:
        print("Error:", e)
        logger.error(e)
        errorCount = errorCount + 1
        if errorCount > errorLimit:
            break
        else:
            time.sleep(sleepSec)
            continue

    latestRecords = len(listData)
    records = latestRecords + records
    logger.info("2、{}条写入文件...".format(latestRecords))

    path = "{}/{}/".format(data_path, app)
    create_path(path)  # 不存在路径进行呢创建

    with open(
        "{}{}_{}.csv".format(
            path,
            app,
            # format_date_to(queryTimes)
            format_date(datetime.now().timestamp() * 1000),
        ),
        "a",
        newline="",
    ) as file:
        fieldnames = [
            "symbol",
            "markPrice",
            "indexPrice",
            "estimatedSettlePrice",
            "lastFundingRate",
            "interestRate",
            "nextFundingTime",
            "time",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(listData, key=lambda x: x["symbol"]):
            writer.writerow(row)

    logger.info("3、{} 抓取数据 {} 条记录...".format(app, records))
    if latestRecords > 0:
        nextFundingTime = listData[0]["nextFundingTime"]
        curTime = listData[0]["time"]
        # 计算下次刷新数据时间，作为执行周期
        nextTimesSec = (nextFundingTime - curTime) // 1000 + 50
        errorCount = 0
        logger.info(
            "4、下次执行时间 {} {}".format(
                format_timestamp(nextFundingTime), nextFundingTime
            )
        )
    logger.info("{} app 结束 --------------------------------- ".format(app))
    time.sleep(nextTimesSec)
