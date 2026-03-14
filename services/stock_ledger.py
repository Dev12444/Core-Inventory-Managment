from extensions import db

class StockLedger(db.Model):
    __tablename__ = "stock_ledger"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    movement_type = db.Column(db.String(10))
    reference = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())