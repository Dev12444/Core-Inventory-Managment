from flask import Blueprint, request, jsonify
from extensions import db
from models.category import Category

category_bp = Blueprint("categories", __name__)


@category_bp.route("/categories", methods=["GET"])
def get_categories():

    categories = Category.query.all()

    return jsonify([
        {"category_id": c.category_id, "name": c.name}
        for c in categories
    ])


@category_bp.route("/categories", methods=["POST"])
def create_category():

    data = request.json

    category = Category(name=data["name"])

    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created"})