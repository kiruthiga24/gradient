from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import OrderLines

order_lines_bp = Blueprint("order_lines", __name__)

@order_lines_bp.route("/order_lines", methods=["GET"])
def get_order_lines():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(OrderLines).all()]
    db.close()
    return jsonify(data), 200

