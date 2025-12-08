from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

order_lines_bp = Blueprint("order_lines", __name__)

@order_lines_bp.route("/order_lines", methods=["GET"])
def get_accounts():
    data = fetch_all("order_lines")
    return jsonify(data), 200
