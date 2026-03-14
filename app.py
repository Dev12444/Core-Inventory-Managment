from flask import Flask
from config import Config
from extensions import db, migrate

from routes.product_routes import product_bp
from routes.operation_routes import operation_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(product_bp)
app.register_blueprint(operation_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)