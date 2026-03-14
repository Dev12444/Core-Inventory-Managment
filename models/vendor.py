from extensions import db

class Vendor(db.Model):
    __tablename__ = "vendors"

    vendor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    gstin = db.Column(db.String(50))