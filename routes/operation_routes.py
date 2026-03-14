from flask import Blueprint, request, jsonify
from models.ledger import StockLedger
from models.product import Product
from models.warehouse import Warehouse
from models.receipt import Receipt
from models.receipt_item import ReceiptItem
from models.delivery import Delivery
from models.transfer import Transfer, TransferLine
from services.stock_service import add_stock, remove_stock
from sqlalchemy import func
from extensions import db
import datetime

operation_bp = Blueprint("operations", __name__)

def generate_reference_id(warehouse_id, operation_type):
    # Format: WH01/REC/001
    warehouse = Warehouse.query.get(warehouse_id)
    if not warehouse:
        raise ValueError("Invalid warehouse")
    
    prefix = f"WH{warehouse.id:02d}"
    type_code = {"receipt": "REC", "delivery": "DEL", "transfer": "TRF"}.get(operation_type, "OP")
    
    # Get next number
    if operation_type == "receipt":
        last = Receipt.query.filter(Receipt.reference.like(f"{prefix}/{type_code}/%")).order_by(Receipt.receipt_id.desc()).first()
    elif operation_type == "delivery":
        last = Delivery.query.filter(Delivery.reference.like(f"{prefix}/{type_code}/%")).order_by(Delivery.delivery_id.desc()).first()
    elif operation_type == "transfer":
        last = Transfer.query.filter(Transfer.reference_id.like(f"{prefix}/{type_code}/%")).order_by(Transfer.id.desc()).first()
    else:
        last = None
    
    if last:
        num = int(last.reference.split("/")[-1]) + 1
    else:
        num = 1
    
    return f"{prefix}/{type_code}/{num:03d}"


# RECEIPT (incoming goods) - REMOVED: Use /operations/receipt/create instead


# DELIVERY (outgoing goods) - REMOVED: Use /operations/delivery/create instead


@operation_bp.route("/operations/history", methods=["GET"])
def movement_history():

    type_filter = request.args.get("type")  # receipt, delivery, transfer, adjustment
    product_id = request.args.get("product_id", type=int)
    warehouse_id = request.args.get("warehouse_id", type=int)

    query = StockLedger.query

    if type_filter:
        if type_filter == "receipt":
            query = query.filter(StockLedger.movement_type == "IN", StockLedger.reference.like("RECEIPT%"))
        elif type_filter == "delivery":
            query = query.filter(StockLedger.movement_type == "OUT", StockLedger.reference.like("DELIVERY%"))
        elif type_filter == "transfer":
            query = query.filter(StockLedger.reference.like("TRANSFER%"))
        elif type_filter == "adjustment":
            query = query.filter(StockLedger.reference.like("ADJUSTMENT%"))

    if product_id:
        query = query.filter(StockLedger.product_id == product_id)
    if warehouse_id:
        query = query.filter(StockLedger.warehouse_id == warehouse_id)

    entries = query.order_by(StockLedger.created_at.desc()).all()

    result = []

    for e in entries:
        result.append({
            "product_id": e.product_id,
            "warehouse_id": e.warehouse_id,
            "change": e.quantity,
            "type": e.movement_type,
            "reference": e.reference,
            "created_at": e.created_at.isoformat() if e.created_at else None
        })

    return jsonify(result)

@operation_bp.route("/inventory/stock", methods=["GET"])
def current_stock():

    product_id = request.args.get("product_id", type=int)
    warehouse_id = request.args.get("warehouse_id", type=int)

    query = db.session.query(
        StockLedger.product_id,
        StockLedger.warehouse_id,
        func.sum(StockLedger.quantity).label("stock")
    )

    if product_id:
        query = query.filter(StockLedger.product_id == product_id)
    if warehouse_id:
        query = query.filter(StockLedger.warehouse_id == warehouse_id)

    stock_data = query.group_by(
        StockLedger.product_id,
        StockLedger.warehouse_id
    ).all()

    result = []

    for row in stock_data:
        result.append({
            "product_id": row.product_id,
            "warehouse_id": row.warehouse_id,
            "stock": row.stock
        })

    return jsonify(result)


@operation_bp.route("/operations/transfer", methods=["POST"])
def transfer_stock():

    data = request.json

    required = ["product_id", "from_warehouse_id", "to_warehouse_id", "qty"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Required fields: {', '.join(required)}"}), 400

    if data["from_warehouse_id"] == data["to_warehouse_id"]:
        return jsonify({"error": "Source and destination warehouse must differ"}), 400

    qty = data["qty"]
    if qty <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    # Deduct from source
    remove_stock(
        product_id=data["product_id"],
        warehouse_id=data["from_warehouse_id"],
        qty=qty,
        reference=data.get("reference", "TRANSFER")
    )

    # Add to destination
    add_stock(
        product_id=data["product_id"],
        warehouse_id=data["to_warehouse_id"],
        qty=qty,
        reference=data.get("reference", "TRANSFER")
    )

    return jsonify({"message": "Stock transferred"})



# TRANSFER DOCUMENTS
@operation_bp.route("/operations/transfer/create", methods=["POST"])
def create_transfer_document():
    data = request.json
    if not data or not data.get("from_warehouse_id") or not data.get("to_warehouse_id") or not data.get("lines"):
        return jsonify({"error": "From warehouse, to warehouse, and lines required"}), 400

    if data["from_warehouse_id"] == data["to_warehouse_id"]:
        return jsonify({"error": "Source and destination warehouse must differ"}), 400

    try:
        reference_id = generate_reference_id(data["from_warehouse_id"], "transfer")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    transfer = Transfer(
        reference_id=reference_id,
        from_warehouse_id=data["from_warehouse_id"],
        to_warehouse_id=data["to_warehouse_id"],
        notes=data.get("notes")
    )

    total_qty = 0
    for line_data in data["lines"]:
        if not all(k in line_data for k in ["product_id", "qty"]):
            return jsonify({"error": "Each line must have product_id and qty"}), 400
        line = TransferLine(
            product_id=line_data["product_id"],
            qty=line_data["qty"]
        )
        transfer.lines.append(line)
        total_qty += line_data["qty"]

    transfer.total_qty = total_qty
    db.session.add(transfer)
    db.session.commit()

    return jsonify({"message": "Transfer created", "id": transfer.id, "reference_id": reference_id}), 201

@operation_bp.route("/operations/transfers", methods=["GET"])
def get_transfers():
    transfers = Transfer.query.order_by(Transfer.created_at.desc()).all()
    result = []
    for t in transfers:
        result.append({
            "id": t.id,
            "reference_id": t.reference_id,
            "from_warehouse_id": t.from_warehouse_id,
            "to_warehouse_id": t.to_warehouse_id,
            "status": t.status,
            "total_qty": t.total_qty,
            "notes": t.notes,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "completed_at": t.completed_at.isoformat() if t.completed_at else None
        })
    return jsonify(result)

@operation_bp.route("/operations/transfer/<int:transfer_id>", methods=["GET"])
def get_transfer(transfer_id):
    transfer = Transfer.query.get_or_404(transfer_id)
    lines = []
    for line in transfer.lines:
        lines.append({
            "product_id": line.product_id,
            "product_name": line.product.name if line.product else None,
            "qty": line.qty
        })

    return jsonify({
        "id": transfer.id,
        "reference_id": transfer.reference_id,
        "from_warehouse_id": transfer.from_warehouse_id,
        "from_warehouse_name": transfer.from_warehouse.name if transfer.from_warehouse else None,
        "to_warehouse_id": transfer.to_warehouse_id,
        "to_warehouse_name": transfer.to_warehouse.name if transfer.to_warehouse else None,
        "status": transfer.status,
        "total_qty": transfer.total_qty,
        "notes": transfer.notes,
        "created_at": transfer.created_at.isoformat() if transfer.created_at else None,
        "completed_at": transfer.completed_at.isoformat() if transfer.completed_at else None,
        "lines": lines
    })


@operation_bp.route("/inventory/adjust", methods=["POST"])
def manual_stock_adjustment():

    data = request.json

    required = ["product_id", "warehouse_id", "qty"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Required fields: {', '.join(required)}"}), 400

    qty = data["qty"]
    reference = data.get("reference", "ADJUSTMENT")

    if qty > 0:
        add_stock(
            product_id=data["product_id"],
            warehouse_id=data["warehouse_id"],
            qty=qty,
            reference=reference
        )
    elif qty < 0:
        remove_stock(
            product_id=data["product_id"],
            warehouse_id=data["warehouse_id"],
            qty=abs(qty),
            reference=reference
        )
    else:
        return jsonify({"message": "No adjustment needed"})

    return jsonify({"message": "Stock adjusted"})


@operation_bp.route("/inventory/out-of-stock", methods=["GET"])
def out_of_stock():

    warehouse_id = request.args.get("warehouse_id", type=int)

    stock_query = (
        db.session.query(
            Product.product_id,
            Product.sku,
            Product.name,
            func.coalesce(func.sum(StockLedger.quantity), 0).label("stock")
        )
        .outerjoin(StockLedger, Product.product_id == StockLedger.product_id)
    )

    if warehouse_id:
        stock_query = stock_query.filter(StockLedger.warehouse_id == warehouse_id)

    stock_query = stock_query.group_by(Product.product_id).having(func.coalesce(func.sum(StockLedger.quantity), 0) <= 0)

    result = []
    for row in stock_query.all():
        result.append({
            "product_id": row.product_id,
            "sku": row.sku,
            "name": row.name,
            "stock": row.stock
        })

    return jsonify(result)


@operation_bp.route("/inventory/value", methods=["GET"])
def inventory_value():

    # Requires Product.cost_price to exist. Returns error if missing.
    if not hasattr(Product, "cost_price"):
        return jsonify({"error": "Inventory value not supported without Product.cost_price"}), 400

    stock_query = (
        db.session.query(
            Product.product_id,
            Product.sku,
            Product.name,
            Product.cost_price,
            func.coalesce(func.sum(StockLedger.quantity), 0).label("stock")
        )
        .outerjoin(StockLedger, Product.product_id == StockLedger.product_id)
        .group_by(Product.product_id)
    )

    total_value = 0
    rows = []

    for row in stock_query.all():
        value = row.stock * (row.cost_price or 0)
        total_value += value
        rows.append({
            "product_id": row.product_id,
            "sku": row.sku,
            "name": row.name,
            "stock": row.stock,
            "cost_price": row.cost_price,
            "value": value
        })

    return jsonify({"total_value": total_value, "items": rows})


@operation_bp.route("/inventory/warehouse-summary", methods=["GET"])
def warehouse_summary():

    summary_query = (
        db.session.query(
            Warehouse.id.label("warehouse_id"),
            Warehouse.name.label("warehouse_name"),
            func.coalesce(func.sum(StockLedger.quantity), 0).label("total_stock"),
            func.count(func.distinct(StockLedger.product_id)).label("product_count")
        )
        .outerjoin(StockLedger, Warehouse.id == StockLedger.warehouse_id)
        .group_by(Warehouse.id)
    )

    result = []
    for row in summary_query.all():
        result.append({
            "warehouse_id": row.warehouse_id,
            "warehouse_name": row.warehouse_name,
            "total_stock": row.total_stock,
            "product_count": row.product_count
        })

    return jsonify(result)


@operation_bp.route("/inventory/low-stock", methods=["GET"])
def low_stock_alerts():

    warehouse_id = request.args.get("warehouse_id", type=int)
    product_id = request.args.get("product_id", type=int)
    sku = request.args.get("sku")

    query = db.session.query(
        StockLedger.product_id,
        StockLedger.warehouse_id,
        func.sum(StockLedger.quantity).label("stock"),
        Product.reorder_level,
        Product.sku,
        Product.name
    ).join(Product, Product.product_id == StockLedger.product_id)

    if warehouse_id:
        query = query.filter(StockLedger.warehouse_id == warehouse_id)
    if product_id:
        query = query.filter(StockLedger.product_id == product_id)
    if sku:
        query = query.filter(Product.sku.ilike(f"%{sku}%"))

    stock_data = query.group_by(
        StockLedger.product_id,
        StockLedger.warehouse_id,
        Product.reorder_level,
        Product.sku,
        Product.name
    ).having(func.sum(StockLedger.quantity) <= Product.reorder_level).all()

    result = []

    for row in stock_data:
        result.append({
            "product_id": row.product_id,
            "sku": row.sku,
            "name": row.name,
            "warehouse_id": row.warehouse_id,
            "stock": row.stock,
            "reorder_level": row.reorder_level
        })

    return jsonify(result)
