# import time
# from apscheduler.schedulers.blocking import BlockingScheduler


# def taskDetail(taskName: str):
#     currTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     print(f"{taskName}-->", "currTime:", currTime)


# if __name__ == "__main__":
#     apSchedule = BlockingScheduler()
#     apSchedule.add_job(func=taskDetail, trigger="interval", seconds=5, args=["task-A"])

#     apSchedule.start()
