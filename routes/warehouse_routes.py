from flask import Blueprint, request, jsonify
from extensions import db
from models.warehouse import Warehouse

warehouse_bp = Blueprint("warehouses", __name__)


@warehouse_bp.route("/warehouses", methods=["POST"])
def create_warehouse():

    data = request.json

    warehouse = Warehouse(
        name=data["location_name"]
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
            "id": w.warehouse_id,
            "name": w.location_name
        })

    return jsonify(result)