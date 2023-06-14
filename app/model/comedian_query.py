from sqlalchemy import func
from app.model import db

from app.model.comedian import Comedian
from app.model.video import Video

def getComedianNames():
    return (
        db.session.query(Comedian.id, Comedian.name, func.count(Video.id))
            .join(Video)
            .group_by(Comedian.id)
            .order_by(Comedian.name.asc())
            .all()
    )


def getComedianById(comedian_id):
    return db.session.query(Comedian).filter_by(id=comedian_id).first()