from extensions import db

class Unit(db.Model):

    __tablename__ = "units"

    unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))