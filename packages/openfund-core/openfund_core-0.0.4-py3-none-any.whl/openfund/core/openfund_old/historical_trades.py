#!/usr/bin/env python
import csv
import logging
import time
import os
import sys

from datetime import datetime

from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.error import ClientError, Error

import enums as enums
from time_tools import format_timestamp
from file_tools import create_path
from prepare_env import get_api_key, get_path

# config_logging(logging, logging.INFO)
api_key, api_secret = get_api_key()
um_futures_client = UMFutures(key=api_key)

data_path, log_path = get_path()
# POOL = ['AAVEUSDT','BTCBUSD', 'BTCDOMUSDT', 'BTCSTUSDT', 'BTCUSDT', 'BTCUSDT_231229', 'BTCUSDT_240329',
#         'BLURUSDT', 'DYDXUSDT', 'ETHBTC', 'ETHBUSD', 'ETHUSDT', 'ETHUSDT_231229', 'ETHUSDT_240329',
#         'GMTBUSD', 'GMTUSDT', 'LTCBUSD', 'LTCUSDT', 'MATICBUSD', 'MATICUSDT', 'SOLBUSD', 'SOLUSDT',
#         ]
POOL = ["GMTBUSD"]

# 历史截止数据开关
hisSwitch = 1
# hisSwitch 打开的情况下，抓取数据截止时间
hisDateTime = 1653974399999

for symbol in POOL:
    logging.basicConfig(
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        filename="{}/{}_historical_trades_{}.log".format(
            log_path, symbol, format_timestamp(datetime.now().timestamp() * 1000)
        ),
    )
    logging.info("{} symbol 开始 ++++++++++++++++++++++++++++ ".format(symbol))

    latestRecords = 1
    records = 0  # 累计记录数
    queryTimes = 0  # 执行次数
    nextKey = 0
    params = {"limit": 1000}

    while latestRecords != 0:  # 循环读取，直到记录为空
        queryTimes = queryTimes + 1
        if nextKey != 0:
            params = {"limit": 1000, "fromId": nextKey}

        logging.info("1、{}第{}次开始执行...".format(symbol, queryTimes))
        listData = []
        try:
            listData = um_futures_client.historical_trades(symbol, **params)
        # except ClientError as error:
        #     logging.error(
        #         "Found error. status: {}, error code: {}, error message: {}".format(
        #             error.status_code, error.error_code, error.error_message
        #         )
        #     )
        #     time.sleep(30)
        #     continue
        # except ProxyError as error:
        #     logging.error(
        #         "Found error. error code: {}, error message: {}".format(
        #             error, error.error_message
        #         )
        #     )
        #     time.sleep(10)
        #     continue
        except Exception as e:
            print("Error:", e)
            logging.error(e)
            time.sleep(10)
            continue
        # listData 结构
        # [
        #     {
        #         "id": 28457,
        #         "price": "4.00000100",
        #         "qty": "12.00000000",
        #         "quoteQty": "8000.00",
        #         "time": 1499865549590,
        #         "isBuyerMaker": true,
        #     }
        # ]
        latestRecords = len(listData)
        records = latestRecords + records
        logging.info("2、{}条写入文件...".format(latestRecords))

        path = "{}/historical_trades/{}/".format(data_path, symbol)

        create_path(path)  # 不存在路径进行呢创建

        with open(
            "{}/{}_historical_trades.csv".format(path, symbol), "a", newline=""
        ) as file:
            writer = csv.writer(file)
            # 时间戳倒序，插入文件尾部
            writer.writerows(sorted(listData, key=lambda x: x["id"], reverse=True))

        # 拿到最后一条记录后,获取close时间戳,变为下一次截止时间戳
        if latestRecords > 0:
            first = listData[0]
            nextKey = first["id"] - 1000
            curTime = first["time"]
            logging.info("3、下个Key {} {}".format(format_timestamp(curTime), nextKey))
            errorCount = 0
            if curTime <= hisDateTime and hisSwitch == 1:
                break
        else:
            logging.info("4、结束...")

        time.sleep(0.01)

    logging.info("5、{} 抓取数据 {} 条记录...".format(symbol, records))
    logging.info("{} symbol --------------------------------- ".format(symbol))
