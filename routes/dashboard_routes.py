from flask import Blueprint, jsonify
from extensions import db
from models.product import Product
from models.warehouse import Warehouse
from models.ledger import StockLedger
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():

    total_products = Product.query.count()
    total_warehouses = Warehouse.query.count()
    total_movements = StockLedger.query.count()

    # low stock products
    low_stock = db.session.query(Product).all()

    low_stock_list = []

    for p in low_stock:

        stock = db.session.query(
            func.sum(StockLedger.quantity)
        ).filter(
            StockLedger.product_id == p.product_id
        ).scalar()

        stock = stock or 0

        if stock <= p.reorder_level:
            low_stock_list.append({
                "product_id": p.product_id,
                "name": p.name,
                "sku": p.sku,
                "stock": stock,
                "reorder_level": p.reorder_level
            })

    return jsonify({
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "total_movements": total_movements,
        "low_stock_products": low_stock_list
    })