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
