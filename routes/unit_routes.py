from flask import Blueprint, request, jsonify
from extensions import db
from models.unit import Unit

unit_bp = Blueprint("units", __name__)


@unit_bp.route("/units", methods=["GET"])
def get_units():

    units = Unit.query.all()

    return jsonify([
        {"unit_id": u.unit_id, "name": u.name}
        for u in units
    ])


@unit_bp.route("/units", methods=["POST"])
def create_unit():

    data = request.json

    unit = Unit(name=data["name"])

    db.session.add(unit)
    db.session.commit()

    return jsonify({"message": "Unit created"})