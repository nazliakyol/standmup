from datetime import time
from apscheduler.schedulers.background import BackgroundScheduler
from app.service.videos import addVideoAuto
from app.service.youtube import runYoutubeAuto

scheduler = None

def start_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    runYoutubeAuto_time = time(hour=17, minute=0, second=0)
    addVideoAuto_time = time(hour=18, minute=0, second=0)

    scheduler.add_job(runYoutubeAuto, 'cron', day_of_week ='*', hour=runYoutubeAuto_time.hour, minute=runYoutubeAuto_time.minute, second=runYoutubeAuto_time.second, id='my_new_link')
    scheduler.add_job(addVideoAuto, 'cron', day_of_week ='*', hour=addVideoAuto_time.hour, minute= addVideoAuto_time.minute, second= addVideoAuto_time.second, id='my_new_video')

    scheduler.start()