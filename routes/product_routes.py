from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from sqlalchemy import func
from models.ledger import StockLedger

product_bp = Blueprint("products", __name__)


# CREATE PRODUCT
@product_bp.route("/products", methods=["POST"])
def create_product():

    data = request.json

    if not data or not data.get("name") or not data.get("sku"):
        return jsonify({"error": "Name and SKU are required"}), 400

    product = Product(
        name=data["name"],
        sku=data["sku"],
        category=data.get("category"),
        unit=data.get("unit"),
        reorder_level=data.get("reorder_level", 10)
    )

    from sqlalchemy.exc import IntegrityError

    try:
        db.session.add(product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SKU already exists"}), 400

    return jsonify({
        "message": "Product created",
        "product_id": product.product_id
    }), 201


# UPDATE PRODUCT
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    product = Product.query.get_or_404(product_id)
    data = request.json

    product.name = data.get("name", product.name)
    product.category = data.get("category", product.category)
    product.unit = data.get("unit", product.unit)
    product.reorder_level = data.get("reorder_level", product.reorder_level)

    db.session.commit()

    return jsonify({"message": "Product updated"})


# GET ALL PRODUCTS
@product_bp.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()

    result = []

    for p in products:
        result.append({
            "product_id": p.product_id,
            "name": p.name,
            "sku": p.sku,
            "category": p.category,
            "unit": p.unit,
            "reorder_level": p.reorder_level
        })

    return jsonify(result)


# SEARCH PRODUCT BY SKU
@product_bp.route("/products/search", methods=["GET"])
def search_product():

    sku = request.args.get("sku")

    if not sku:
        return jsonify({"error": "SKU query required"}), 400

    products = Product.query.filter(Product.sku.like(f"%{sku}%")).all()

    result = []

    for p in products:
        result.append({
            "product_id": p.product_id,
            "name": p.name,
            "sku": p.sku
        })

    return jsonify(result)
