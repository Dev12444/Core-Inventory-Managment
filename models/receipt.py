from extensions import db


class Receipt(db.Model):

    __tablename__ = "receipts"

    receipt_id = db.Column(db.Integer, primary_key=True)

    reference = db.Column(db.String(50), unique=True)

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendors.vendor_id")
    )

    warehouse_id = db.Column(
        db.Integer,
        db.ForeignKey("warehouses.id")
    )

    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
