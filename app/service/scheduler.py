from datetime import time
from apscheduler.schedulers.background import BackgroundScheduler
from app.service.videos import addVideoAuto
from app.service.youtube import runYoutubeAuto

scheduler = None

def start_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    target_time = time(hour=17, minute=0, second=0)

    scheduler.add_job(addVideoAuto, 'interval', hours=12, id='my_new_video')
    scheduler.add_job(runYoutubeAuto, 'cron', day_of_week ='*', hour=target_time.hour, minute=target_time.minute, second=target_time.second, id='my_new_link')

    scheduler.start()