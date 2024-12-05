#!/usr/bin/env python
import csv
import logging
import time
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from datetime import datetime
from binance.um_futures import UMFutures
from binance.error import ClientError
from libs.time_tools import format_timestamp
from libs.file_tools import create_path
from libs.prepare_env import get_api_key, get_path
from libs import enums

data_path, log_path = get_path()
um_futures_client = UMFutures()

POOL = enums.CUR_SYMBOL_POOL
interval = enums.KLINE_INTERVAL_5MINUTE
# 历史截止数据开关
hisSwitch = 0
# hisSwitch 打开的情况下，抓取数据截止时间
hisDateTime = 1653974399999
# 发现异常后累计失败次数上限，超过后退出。
errorLimit = 100
# 异常后暂停秒数
sleepSec = 10

app = "mark_price_klines"

for symbol in POOL:
    fileName = "{}/{}_{}_{}.log".format(
        log_path, symbol, app, format_timestamp(datetime.now().timestamp() * 1000)
    )
    logging.basicConfig(
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        filename=fileName,
    )
    logging.info("{}_symbol 开始 ++++++++++++++++++++++++++++ ".format(symbol))

    latestRecords = 1
    records = 0  # 累计记录数
    queryTimes = 0  # 执行次数
    nextEndTime = 0  # 下次结束时间
    errorCount = 0  # 异常次数
    params = {"limit": 1000}
    while latestRecords != 0:  # 循环读取，直到记录为空
        queryTimes = queryTimes + 1
        if nextEndTime != 0:
            params = {"limit": 1000, "endTime": nextEndTime}

        logging.info("1、{}第{}次开始执行...".format(symbol, queryTimes))
        listData = []
        try:
            listData = um_futures_client.mark_price_klines(symbol, interval, **params)
        except KeyError as err:
            print("KeyError:", err)
            logging.error(err)
            break
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            if error.error_code == -4144 and error.status_code == 400:
                break
        except Exception as e:
            print("Error:", e)
            logging.error(e)
            errorCount = errorCount + 1
            if errorCount > errorLimit:
                break
            else:
                time.sleep(sleepSec)
                continue

        latestRecords = len(listData)
        records = latestRecords + records
        logging.info("2、{}条写入文件...".format(latestRecords))

        path = "{}/{}/{}/".format(data_path, app, symbol)
        create_path(path)  # 不存在路径进行呢创建

        with open(
            "{}{}_{}_{}.csv".format(path, app, symbol, interval),
            "a",
            newline="",
        ) as file:
            writer = csv.writer(file)
            # 时间戳倒序，插入文件尾部
            writer.writerows(sorted(listData, key=lambda x: x[0], reverse=True))

        # 拿到最后一条记录后,获取close时间戳,变为下一次截止时间戳
        if latestRecords > 0:
            nextEndTime = (
                listData[0][0] - 1
            )  # -1 不和close时间戳相同，避免重新拉取重复数据
            errorCount = 0
            logging.info(
                "3、下次结束时间 {} {}".format(
                    format_timestamp(nextEndTime), nextEndTime
                )
            )

            if nextEndTime <= hisDateTime and hisSwitch == 1:
                break
        else:
            logging.info("4、结束...")

        # time.sleep(0.1)

    logging.info("5、{} 抓取数据 {} 条记录...".format(symbol, records))
    logging.info("{} symbol --------------------------------- ".format(symbol))
