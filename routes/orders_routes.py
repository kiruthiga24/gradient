from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    data = fetch_all("orders")
    return jsonify(data), 200

@orders_bp.route("/orders", methods=["POST"])
def create_orders():
    data = request.json
    created = insert_record("orders", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

