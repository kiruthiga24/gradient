from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_accounts():
    data = fetch_all("customers")
    return jsonify(data), 200
