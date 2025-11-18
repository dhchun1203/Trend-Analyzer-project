from apscheduler.schedulers.blocking import BlockingScheduler
from crawler.naver_best100 import crawl_naver_best100

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=3)  # 매일 새벽 3시
def job():
    crawl_naver_best100()

scheduler.start()
