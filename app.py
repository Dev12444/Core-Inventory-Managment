from flask import Flask, render_template
from config import Config
from extensions import db
from routes.warehouse_routes import warehouse_bp
from routes.dashboard_routes import dashboard_bp

from models.product import Product
from models.ledger import StockLedger
from models.warehouse import Warehouse
from models.vendor import Vendor
from models.customer import Customer
from models.category import Category
from models.unit import Unit
from models.receipt import Receipt
from models.receipt_item import ReceiptItem
from models.delivery import Delivery
from models.delivery_item import DeliveryItem
from models.transfer import Transfer, TransferLine

from routes.product_routes import product_bp
from routes.operation_routes import operation_bp
from routes.vendor_routes import vendor_bp
from routes.customer_routes import customer_bp
from routes.category_routes import category_bp
from routes.unit_routes import unit_bp
from routes.receipt_routes import receipt_bp
from routes.delivery_routes import delivery_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(operation_bp)
app.register_blueprint(vendor_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(category_bp)
app.register_blueprint(unit_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(warehouse_bp)
app.register_blueprint(receipt_bp)
app.register_blueprint(delivery_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    from flask import request, redirect, url_for
    if request.method == "POST":
        # Accept the login and redirect to the dashboard frontend
        return redirect(url_for("home"))
    return render_template("login.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)