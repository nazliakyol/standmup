from app.model import db
from app.model.comedian import Comedian, comedian_product
from app.model.product import Product

def getProductById(product_id):
    return db.session.query(Product).filter_by(id= product_id).first()

def getProducts():
    return db.session.query(Product).order_by(Product.title.asc()).all()

def getProductsByComedianId(product_id):
    return (
    db.session.query(Comedian).
    join(
        comedian_product, Comedian.id == comedian_product.c.comedian_id
    ).join(
        Product, Product.id == comedian_product.c.product_id
    ).filter(
        Product.id == product_id,
    ).all())



