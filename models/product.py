from extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    reorder_level = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, server_default=db.func.now())