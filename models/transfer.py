from extensions import db

class Transfer(db.Model):
    __tablename__ = "transfers"

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(50), unique=True, nullable=False)
    from_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    to_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, completed
    total_qty = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    completed_at = db.Column(db.DateTime)

    # Relationships
    from_warehouse = db.relationship('Warehouse', foreign_keys=[from_warehouse_id], backref='transfers_from')
    to_warehouse = db.relationship('Warehouse', foreign_keys=[to_warehouse_id], backref='transfers_to')
    lines = db.relationship('TransferLine', backref='transfer', cascade='all, delete-orphan')

class TransferLine(db.Model):
    __tablename__ = "transfer_lines"

    id = db.Column(db.Integer, primary_key=True)
    transfer_id = db.Column(db.Integer, db.ForeignKey('transfers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    # Relationships
    product = db.relationship('Product', backref='transfer_lines')