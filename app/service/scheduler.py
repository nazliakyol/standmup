from apscheduler.schedulers.background import BackgroundScheduler
from app.service.videos import addVideoAuto
from app.service.youtube import runYoutubeAuto

scheduler = None

def start_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()

    scheduler.add_job(addVideoAuto, 'interval', hours=1, id='my_new_video')
    scheduler.add_job(runYoutubeAuto, 'interval', hours=1, id='my_new_link')
    scheduler.start()