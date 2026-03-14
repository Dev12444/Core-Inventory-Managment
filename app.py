from flask import Flask
from config import Config
from extensions import db
from routes.warehouse_routes import warehouse_bp
from routes.dashboard_routes import dashboard_bp

from models.product import Product
from models.ledger import StockLedger
from models.warehouse import Warehouse

from routes.product_routes import product_bp
from routes.operation_routes import operation_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(operation_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(warehouse_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)