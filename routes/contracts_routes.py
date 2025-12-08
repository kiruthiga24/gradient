from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

contracts_bp = Blueprint("contracts", __name__)

@contracts_bp.route("/contracts", methods=["GET"])
def get_accounts():
    data = fetch_all("contracts")
    return jsonify(data), 200
