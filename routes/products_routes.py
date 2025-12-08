from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["GET"])
def get_accounts():
    data = fetch_all("products")
    return jsonify(data), 200
