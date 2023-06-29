from sqlalchemy import func
from app.model import db
from app.model.youtubeLink import YoutubeLink


def getCountByYoutubeLinkId():
    return db.session.query(func.count(YoutubeLink.id)).scalar()
