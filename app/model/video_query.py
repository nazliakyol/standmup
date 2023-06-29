from sqlalchemy import func, desc, or_, not_, distinct
from app.model import db
from app.model.comedian import Comedian
from app.model.tag import Tag
from app.model.video import Video, video_tag


def getVideoById(video_id):
    return db.session.query(Video).filter_by(id=video_id).first()

def getOtherVideos(video_id, limit):
    return (
        db.session.query(Video)
            .filter(Video.is_active)
            .filter(not_(Video.id == video_id))
            .limit(limit)
            .all()
    )

def getVideos(page, pagesSize=10):
    return (
            db.session.query(Video)
                .filter((Video.is_active))
                .order_by(desc(Video.creation_date))
                .limit(pagesSize).offset((page - 1) * pagesSize)
                .all()
        )

def getVideosByComedianId(comedian_id, page, pagesSize=10):
    return (
        db.session.query(Video)
            .filter((Video.is_active))
            .filter_by(comedian_id=comedian_id)
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

def getVideoCountByComedianId(comedian_id):
    return (
        db.session.query(func.count(Video.id))
            .filter(Video.is_active)
            .filter_by(comedian_id=comedian_id)
            .scalar()
    )

def getVideoCountByTagId(tag_id):
    return (db.session.query(func.count(Video.id)).filter(Video.is_active).join(video_tag).filter_by(
        tag_id=tag_id).scalar())

def getAllVideoCount():
    return db.session.query(db.func.count(Video.id)).scalar()

def searchVideos(search, page, pagesSize=10):
    return (
        db.session.query(Video).distinct()
            .filter((Video.is_active))
            .outerjoin(video_tag)
            .outerjoin(Tag)
            .outerjoin(Comedian).filter(
                or_(
                    or_(
                        Video.title.ilike(f"%{search}%"),
                        Video.description.ilike(f"%{search}%"),
                    ),
                    Tag.name.ilike(f"%{search}%"),
                    Comedian.name.ilike(f"%{search}%"),
                )
            ).order_by(desc(Video.creation_date))
            .limit(pagesSize)
            .offset((page - 1) * pagesSize)
            .all()
    )

def getSearchVideoCount(search):
    return (
        db.session.query(db.func.count(distinct(Video.id)))
            .filter(Video.is_active)
            .outerjoin(video_tag)
            .outerjoin(Tag)
            .outerjoin(Comedian).filter(
                or_(
                    or_(
                        Video.title.ilike(f"%{search}%"),
                        Video.description.ilike(f"%{search}%"),
                    ),
                    Tag.name.ilike(f"%{search}%"),
                    Comedian.name.ilike(f"%{search}%"),
    )).scalar()
    )

def getRandomVideo():
    return Video.query.order_by(func.random()).first()