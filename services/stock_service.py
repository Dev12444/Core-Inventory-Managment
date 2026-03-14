from extensions import db
from models.ledger import StockLedger


def add_stock(product_id, warehouse_id, qty, reference):

    entry = StockLedger(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=qty,
        movement_type="IN",
        reference=reference
    )

    db.session.add(entry)
    db.session.commit()


def remove_stock(product_id, warehouse_id, qty, reference):

    entry = StockLedger(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=-qty,
        movement_type="OUT",
        reference=reference
    )

    db.session.add(entry)
    db.session.commit()