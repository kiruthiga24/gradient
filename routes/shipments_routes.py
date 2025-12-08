from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

shipments_bp = Blueprint("shipments", __name__)

@shipments_bp.route("/shipments", methods=["GET"])
def get_accounts():
    data = fetch_all("shipments")
    return jsonify(data), 200
