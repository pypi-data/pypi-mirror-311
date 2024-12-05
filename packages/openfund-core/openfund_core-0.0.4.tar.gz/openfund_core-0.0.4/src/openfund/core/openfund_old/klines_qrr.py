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
from libs.time_tools import format_timestamp
from libs.file_tools import create_path
from libs import enums
from libs import email_tools
from libs.log_tools import Logger

nextTimeMin = 5
um_futures_client = UMFutures()
app = "klines_qrr"
logger = Logger(app).get_log()
# logger.basicConfig(
#     format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logger.INFO,
#     filename="{0}/{1}_{2}.log".format(
#         log_path, app, format_timestamp(datetime.now().timestamp() * 1000)
#     ),
# )


def job():
    content = ""
    dateTime = ""
    threshold = 10
    POOL = enums.NEW_SYMBOL_POLL
    interval = enums.KLINE_INTERVAL_5MINUTE

    for symbol in POOL:
        logger.info(
            "{} symbol 开始计算量比 ++++++++++++++++++++++++++++ ".format(symbol)
        )
        params = {"limit": 2}
        listData = []
        try:
            listData = um_futures_client.klines(symbol, interval, **params)
        except Exception as e:
            print("Error:", e)
            logger.error("UM_FUTURES_CLIENT:", e)
            time.sleep(10)
            continue
        latestRecords = len(listData)
        logger.info("1、{} 获取数据 {} 条记录...".format(symbol, latestRecords))
        # 计算量比
        if latestRecords > 0:
            qrr = 0
            vol1 = float(listData[0][5])
            vol2 = float(listData[1][5])
            if vol2 != 0.0:
                qrr = round(float(listData[0][5]) / float(listData[1][5]), 1)

            lastTime = format_timestamp(listData[1][6])
            curTime = format_timestamp(listData[0][6])

            logger.info(
                "2、{0} {2} ~ {3} 量比 = {1} ".format(symbol, qrr, lastTime, curTime)
            )

            if qrr >= threshold:
                content = content + "{0} 量比QRR={1}> {4} ({2}/{3}={1})\n".format(
                    symbol, qrr, vol1, vol2, threshold
                )
                dateTime = "在[{0} ~ {1}]:\n".format(lastTime, curTime)

        logger.info("{} symbol --------------------------------- ".format(symbol))

    if content != "":
        content = dateTime + content
        logger.info("content:\n{}".format(content))
        repeat = 3
        while repeat > 0:
            try:
                email_tools.mail("QRR", content)
                logger.info("Sender @Mail =========================== ")
                repeat = 0  # 成功发送重置
            except Exception as e:
                print("Mail_Error:", e)
                logger.error("EMAIL_TOOLS:", e)
                repeat = repeat - 1  # 失败情况下重试3次

    else:
        logger.info("No Send Msg!")


if __name__ == "__main__":
    schedule.every(nextTimeMin).minutes.do(job)
    logger.info("Schedule Starting min ...... ".format(nextTimeMin))
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
