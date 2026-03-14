from flask import Blueprint, request, jsonify
from extensions import db
from models.customer import Customer

customer_bp = Blueprint("customers", __name__)


@customer_bp.route("/customers", methods=["GET"])
def get_customers():

    customers = Customer.query.all()

    return jsonify([
        {"customer_id": c.customer_id, "name": c.name, "contact": c.contact, "phone": c.phone, "email": c.email, "gstin": c.gstin}
        for c in customers
    ])


@customer_bp.route("/customers", methods=["POST"])
def create_customer():

    data = request.json

    customer = Customer(
        name=data["name"],
        contact=data.get("contact"),
        phone=data.get("phone"),
        email=data.get("email"),
        gstin=data.get("gstin")
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created"})