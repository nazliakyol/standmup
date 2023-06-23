from app.model import db
from app.model.comedian import Comedian
from app.model.product import Product


def getProductById(product_id):
    return db.session.query(Product).filter_by(id=product_id).first()


def getProducts():
    return db.session.query(Product).order_by(Product.title.asc()).all()


def getProductsByComedianId(comedian_id):
    return (
        db.session.query(Product)
            .join(Comedian)
            .filter_by(id=comedian_id).all()
    )
