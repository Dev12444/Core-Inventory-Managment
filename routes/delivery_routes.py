from flask import Blueprint, request, jsonify
from extensions import db

from models.delivery import Delivery
from models.delivery_item import DeliveryItem
from models.ledger import StockLedger


delivery_bp = Blueprint("deliveries", __name__)


@delivery_bp.route("/operations/delivery/create", methods=["POST"])
def create_delivery():

    data = request.json

    delivery = Delivery(
        customer_id=data["customer_id"],
        warehouse_id=data["warehouse_id"]
    )

    db.session.add(delivery)
    db.session.flush()

    for item in data["items"]:

        d_item = DeliveryItem(
            delivery_id=delivery.delivery_id,
            product_id=item["product_id"],
            quantity=item["qty"]
        )

        db.session.add(d_item)

    db.session.commit()

    return jsonify({"message": "Delivery created"})


@delivery_bp.route("/operations/delivery/ship/<int:id>", methods=["POST"])
def ship_delivery(id):

    delivery = Delivery.query.get_or_404(id)

    items = DeliveryItem.query.filter_by(
        delivery_id=id
    ).all()

    for item in items:

        ledger = StockLedger(
            product_id=item.product_id,
            warehouse_id=delivery.warehouse_id,
            quantity=-item.quantity,
            movement_type="delivery"
        )

        db.session.add(ledger)

    delivery.status = "done"

    db.session.commit()

    return jsonify({"message": "Delivery shipped"})