from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

usage_metrics_bp = Blueprint("usage_metrics", __name__)

@usage_metrics_bp.route("/usage_metrics", methods=["GET"])
def get_accounts():
    data = fetch_all("usage_metrics")
    return jsonify(data), 200
