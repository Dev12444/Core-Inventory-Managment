from extensions import db

class Product(db.Model):

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, server_default=db.func.now())