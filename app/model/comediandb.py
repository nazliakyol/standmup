from app.model.db import db, application

# data comedian
class Comedian(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    video = db.relationship("Video", backref="comedian")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

with application.app_context():
    db.create_all()