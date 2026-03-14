from flask import Blueprint, request, jsonify
from extensions import db
from models.vendor import Vendor

vendor_bp = Blueprint("vendors", __name__)


@vendor_bp.route("/vendors", methods=["GET"])
def get_vendors():

    vendors = Vendor.query.all()

    return jsonify([
        {"vendor_id": v.vendor_id, "name": v.name, "contact": v.contact, "phone": v.phone, "email": v.email, "gstin": v.gstin}
        for v in vendors
    ])


@vendor_bp.route("/vendors", methods=["POST"])
def create_vendor():

    data = request.json

    vendor = Vendor(
        name=data["name"],
        contact=data.get("contact"),
        phone=data.get("phone"),
        email=data.get("email"),
        gstin=data.get("gstin")
    )

    db.session.add(vendor)
    db.session.commit()

    return jsonify({"message": "Vendor created"})


@vendor_bp.route("/vendors/<int:id>", methods=["PUT"])
def update_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    data = request.json

    vendor.name = data.get("name", vendor.name)
    vendor.contact = data.get("contact", vendor.contact)
    vendor.phone = data.get("phone", vendor.phone)
    vendor.email = data.get("email", vendor.email)
    vendor.gstin = data.get("gstin", vendor.gstin)

    db.session.commit()

    return jsonify({"message": "Vendor updated"})


@vendor_bp.route("/vendors/<int:id>", methods=["DELETE"])
def delete_vendor(id):
    vendor = Vendor.query.get_or_404(id)

    db.session.delete(vendor)
    db.session.commit()

    return jsonify({"message": "Vendor deleted"})