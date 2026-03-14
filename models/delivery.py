from extensions import db


class Delivery(db.Model):

    __tablename__ = "deliveries"

    delivery_id = db.Column(db.Integer, primary_key=True)

    reference = db.Column(db.String(50), unique=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.customer_id")
    )

    warehouse_id = db.Column(
        db.Integer,
        db.ForeignKey("warehouses.id")
    )

    status = db.Column(db.String(20), default="draft")

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )