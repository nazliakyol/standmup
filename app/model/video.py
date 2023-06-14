from datetime import datetime
from sqlalchemy import DateTime
from app.model import db
from app.model.tag import Tag

video_tag = db.Table('video_tag',
                     db.Column('video_id', db.String(36), db.ForeignKey('video.id')),
                     db.Column('tag_id', db.String(36), db.ForeignKey('tag.id'))
                     )

# data video link
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comedian_id = db.Column(db.String(36), db.ForeignKey("comedian.id"))
    title = db.Column(db.String(512), unique=False, nullable=False)
    link = db.Column(db.String(512), nullable=False, unique=True)
    creation_date = db.Column(DateTime(timezone=True), default=db.func.current_timestamp())
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_ready = db.Column(db.Boolean, default=True)
    tags = db.relationship('Tag', secondary=video_tag, backref='tagged')


    def __init__(self, comedian_id, title, link, description, is_active, is_ready):
        self.comedian_id = comedian_id
        self.title = title
        self.link = link
        self.description = description
        self.is_active = is_active
        self.is_ready = is_ready

        self.tags = []

    def getTags(self):
        tags = db.session.query(Tag).join(video_tag).join(Video).filter(
            video_tag.c.video_id == self.id).order_by(Tag.name.asc()).limit(6).all()
        return tags

    def to_dict(self):
        return {
            "comedian_id": self.comedian_id,
            "title": self.title,
            "link": self.link,
            "tags": self.getTags(),
            "creation_date": {'self.creation_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')},
            "comedian_name": self.comedian.name,
            "description": self.description,
            "is_active": self.is_active,
            "is_ready": self.is_ready

        }
