from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["GET"])
def get_accounts():
    data = fetch_all("orders")
    return jsonify(data), 200
