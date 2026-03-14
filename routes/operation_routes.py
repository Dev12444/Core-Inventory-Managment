from flask import Blueprint, request, jsonify
from services.stock_service import add_stock, remove_stock

operation_bp = Blueprint("operations", __name__)


# RECEIPT (incoming goods)
@operation_bp.route("/operations/receipt", methods=["POST"])
def create_receipt():

    data = request.json

    if not data or "items" not in data:
        return jsonify({"error": "Items required"}), 400

    items = data["items"]

    for item in items:
        add_stock(
            product_id=item["product_id"],
            warehouse_id=item["warehouse_id"],
            qty=item["qty"],
            reference="RECEIPT"
        )

    return jsonify({"message": "Stock added successfully"})


# DELIVERY (outgoing goods)
@operation_bp.route("/operations/delivery", methods=["POST"])
def create_delivery():

    data = request.json

    if not data or "items" not in data:
        return jsonify({"error": "Items required"}), 400

    items = data["items"]

    for item in items:
        remove_stock(
            product_id=item["product_id"],
            warehouse_id=item["warehouse_id"],
            qty=item["qty"],
            reference="DELIVERY"
        )

    return jsonify({"message": "Stock deducted successfully"})