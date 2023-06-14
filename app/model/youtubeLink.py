from app.model import db

# data youtubeLink
class YoutubeLink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    youtube_link = db.Column(db.Text, nullable=False, unique=True)
    message = db.Column(db.Text, nullable=True)

    def __init__(self, youtube_link, message):
        self.youtube_link = youtube_link
        self.message = message

    def to_dict(self):
        return {"id": self.id, "youtube_link": self.youtube_link, "message": self.message}

