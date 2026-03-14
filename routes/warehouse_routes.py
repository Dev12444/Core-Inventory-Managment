from flask import Blueprint, request, jsonify
from extensions import db
from models.warehouse import Warehouse

warehouse_bp = Blueprint("warehouses", __name__)


@warehouse_bp.route("/warehouses", methods=["POST"])
def create_warehouse():

    data = request.json

    if not data or not data.get("name"):
        return jsonify({"error": "Warehouse name is required"}), 400

    warehouse = Warehouse(
        name=data["name"],
        location=data.get("location")
    )

    db.session.add(warehouse)
    db.session.commit()

    return jsonify({"message": "Warehouse created"})


@warehouse_bp.route("/warehouses", methods=["GET"])
def get_warehouses():

    warehouses = Warehouse.query.all()

    result = []

    for w in warehouses:
        result.append({
            "id": w.id,
            "name": w.name,
            "location": w.location
        })

    return jsonify(result)