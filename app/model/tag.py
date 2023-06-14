from sqlalchemy import func
from app.model import db

# data tag
class Tag(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, id, name, is_visible):
        self.id = id
        self.name = name
        self.is_visible = is_visible

    def to_dict(self):
        return {"id": self.id, "name": self.name, "is_visible": self.is_visible}

    def to_url(self):
        if ' ' in self.name:
            return self.name.replace(' ', '-')
        else:
            return self.name

from app.model.video import Video, video_tag

def getTags():
    return db.session.query(Tag).order_by(Tag.name.asc()).all()


def getTagsWithCounts(countMoreThan=5):
    return (
        db.session.query(
            Tag.name,
            func.count(Video.id)
        ).join(
            video_tag,
            Tag.id == video_tag.c.tag_id
        ).join(
            Video,
            Video.id == video_tag.c.video_id
        ).group_by(Tag.name)
        .having(func.count(Video.id)>=countMoreThan)
        .all()
    )