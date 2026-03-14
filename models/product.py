from extensions import db

class Product(db.Model):

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))

    cost_price = db.Column(db.Float)      # purchase price
    selling_price = db.Column(db.Float)   # selling price

    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    category = db.relationship('Category', backref='products')
    unit = db.relationship('Unit', backref='products')