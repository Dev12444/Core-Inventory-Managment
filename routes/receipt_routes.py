from flask import Blueprint, request, jsonify
from extensions import db

from models.receipt import Receipt
from models.receipt_item import ReceiptItem
from models.ledger import StockLedger


receipt_bp = Blueprint("receipts", __name__)


@receipt_bp.route("/operations/receipt/create", methods=["POST"])
def create_receipt():

    data = request.json

    receipt = Receipt(
        vendor_id=data["vendor_id"],
        warehouse_id=data["warehouse_id"]
    )

    db.session.add(receipt)
    db.session.flush()

    for item in data["items"]:

        receipt_item = ReceiptItem(
            receipt_id=receipt.receipt_id,
            product_id=item["product_id"],
            quantity=item["qty"]
        )

        db.session.add(receipt_item)

    db.session.commit()

    return jsonify({
        "message": "Receipt created",
        "receipt_id": receipt.receipt_id
    })


@receipt_bp.route("/operations/receipt/validate/<int:id>", methods=["POST"])
def validate_receipt(id):

    receipt = Receipt.query.get_or_404(id)

    items = ReceiptItem.query.filter_by(
        receipt_id=id
    ).all()

    for item in items:

        ledger = StockLedger(
            product_id=item.product_id,
            warehouse_id=receipt.warehouse_id,
            quantity=item.quantity,
            movement_type="receipt"
        )

        db.session.add(ledger)

    receipt.status = "done"

    db.session.commit()

    return jsonify({"message": "Receipt validated"})


@receipt_bp.route("/operations/receipts", methods=["GET"])
def get_receipts():

    receipts = Receipt.query.all()

    return jsonify([
        {
            "receipt_id": r.receipt_id,
            "reference": r.reference,
            "status": r.status,
            "warehouse_id": r.warehouse_id
        }
        for r in receipts
    ])
