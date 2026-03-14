from app import app
from extensions import db
from models.vendor import Vendor
from models.warehouse import Warehouse
from models.product import Product
from models.category import Category
from models.unit import Unit

with app.app_context():
    db.create_all()
    
    # Create test data
    vendor = Vendor(name='Test Vendor', contact='John', phone='1234567890', email='john@test.com', gstin='GST123')
    db.session.add(vendor)
    
    warehouse = Warehouse(name='Main Warehouse', location='Downtown')
    db.session.add(warehouse)
    
    category = Category(name='Electronics')
    db.session.add(category)
    
    unit = Unit(name='Piece')
    db.session.add(unit)
    
    product1 = Product(sku='PROD001', name='Product 1', category_id=1, unit_id=1, cost_price=10.0, selling_price=15.0)
    product2 = Product(sku='PROD002', name='Product 2', category_id=1, unit_id=1, cost_price=20.0, selling_price=25.0)
    db.session.add(product1)
    db.session.add(product2)
    
    db.session.commit()
    print('Test data created')