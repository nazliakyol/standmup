from app.model import db

comedian_product = db.Table('comedian_product',
                         db.Column('comedian_id', db.String(36), db.ForeignKey('comedian.id')),
                         db.Column('product_id', db.String(36), db.ForeignKey('product.id'))
                         )


class Comedian(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    video = db.relationship("Video", backref="comedian")
    products = db.relationship("Product", secondary=comedian_product, backref='linked')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
