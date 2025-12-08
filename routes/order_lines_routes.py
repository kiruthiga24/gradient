from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

order_lines_bp = Blueprint("order_lines", __name__)

@order_lines_bp.route("/order_lines", methods=["GET"])
def get_order_lines():
    data = fetch_all("order_lines")
    return jsonify(data), 200

@order_lines_bp.route("/order_lines", methods=["POST"])
def create_order_lines():
    data = request.json
    created = insert_record("order_lines", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

