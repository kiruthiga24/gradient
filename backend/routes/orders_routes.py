from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Orders

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Orders).all()]
    db.close()
    return jsonify(data), 200

