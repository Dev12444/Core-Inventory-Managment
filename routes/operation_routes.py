from flask import Blueprint, request, jsonify
from models.ledger import StockLedger
from services.stock_service import add_stock, remove_stock
from sqlalchemy import func
from extensions import db

operation_bp = Blueprint("operations", __name__)


# RECEIPT (incoming goods)
@operation_bp.route("/operations/receipt", methods=["POST"])
def create_receipt():

    data = request.json

    if "items" in data:
        items = data["items"]
    elif "product_id" in data:
        items = [data]
    else:
        return jsonify({"error": "Items required"}), 400

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

    if "items" in data:
        items = data["items"]
    elif "product_id" in data:
        items = [data]
    else:
        return jsonify({"error": "Items required"}), 400

    for item in items:
        remove_stock(
            product_id=item["product_id"],
            warehouse_id=item["warehouse_id"],
            qty=item["qty"],
            reference="DELIVERY"
        )

    return jsonify({"message": "Stock deducted successfully"})

@operation_bp.route("/operations/receipt", methods=["POST"])
def receipt():

    data = request.json

    add_stock(
        product_id=data["product_id"],
        warehouse_id=data["warehouse_id"],
        qty=data["qty"],
        reference=data.get("reference", "Receipt")
    )

    return jsonify({"message": "Stock received"})



@operation_bp.route("/operations/history", methods=["GET"])
def movement_history():

    entries = StockLedger.query.all()

    result = []

    for e in entries:
        result.append({
            "product_id": e.product_id,
            "warehouse_id": e.warehouse_id,
            "change": e.quantity,
            "type": e.movement_type,
            "reference": e.reference
        })

    return jsonify(result)

@operation_bp.route("/inventory/stock", methods=["GET"])
def current_stock():

    stock_data = db.session.query(
        StockLedger.product_id,
        StockLedger.warehouse_id,
        func.sum(StockLedger.quantity).label("stock")
    ).group_by(
        StockLedger.product_id,
        StockLedger.warehouse_id
    ).all()

    result = []

    for row in stock_data:
        result.append({
            "product_id": row.product_id,
            "warehouse_id": row.warehouse_id,
            "stock": row.stock
        })

    return jsonify(result)