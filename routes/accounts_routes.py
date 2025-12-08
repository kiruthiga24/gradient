from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/accounts", methods=["GET"])
def get_accounts():
    data = fetch_all("accounts")
    return jsonify(data), 200
