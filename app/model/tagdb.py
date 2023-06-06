from app.model.db import db, application

# data tag
class Tag(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

with application.app_context():
    db.create_all()