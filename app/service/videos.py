from sqlalchemy import desc
from app.model import video, db
from flask import current_app

def addVideoAuto():
    with current_app.app_context():
        new_video = db.session.query(video.Video).filter_by(is_active=0).filter_by(is_ready=1).order_by(
            desc(video.Video.creation_date)).first()
        if new_video:
            new_video.is_active = 1
            db.session.add(new_video)
            db.session.commit()
        else:
            print("No new video at the moment.")