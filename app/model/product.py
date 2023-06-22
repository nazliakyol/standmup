from app.model import db

# data link
class Product(db.Model):
    id = db.Column(db.String(36), primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    product_link = db.Column(db.String(250), unique=True,  nullable=False)
    image_link = db.Column(db.String(250), unique=False,  nullable=False)

    def __init__(self, id, title, product_link, image_link ):
        self.id = id
        self.title = title
        self.product_link = product_link
        self.image_link = image_link

    def to_dict(self):
        return {"id": self.id, "title": self.title, "product_link": self.product_link, "image_link" : self.image_link}


