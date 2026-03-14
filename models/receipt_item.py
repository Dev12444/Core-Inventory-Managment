from extensions import db


class ReceiptItem(db.Model):

    __tablename__ = "receipt_items"

    item_id = db.Column(db.Integer, primary_key=True)

    receipt_id = db.Column(
        db.Integer,
        db.ForeignKey("receipts.receipt_id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id")
    )

    quantity = db.Column(db.Integer)