from extensions import db
from services.stock_ledger import StockLedger


def add_stock(product_id, warehouse_id, qty, reference):
    """
    Adds stock to the ledger (incoming stock)
    """

    ledger_entry = StockLedger(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=qty,
        movement_type="IN",
        reference=reference
    )

    db.session.add(ledger_entry)
    db.session.commit()


def remove_stock(product_id, warehouse_id, qty, reference):
    """
    Removes stock from the ledger (outgoing stock)
    """

    ledger_entry = StockLedger(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=-qty,
        movement_type="OUT",
        reference=reference
    )

    db.session.add(ledger_entry)
    db.session.commit()