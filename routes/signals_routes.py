from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

signals_bp = Blueprint("signals", __name__)

@signals_bp.route("/signals", methods=["GET"])
def get_accounts():
    data = fetch_all("signals")
    return jsonify(data), 200
