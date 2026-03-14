from extensions import db


class DeliveryItem(db.Model):

    __tablename__ = "delivery_items"

    item_id = db.Column(db.Integer, primary_key=True)

    delivery_id = db.Column(
        db.Integer,
        db.ForeignKey("deliveries.delivery_id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id")
    )

    quantity = db.Column(db.Integer)