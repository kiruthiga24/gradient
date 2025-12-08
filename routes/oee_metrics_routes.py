from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

oee_metrics_bp = Blueprint("oee_metrics", __name__)

@oee_metrics_bp.route("/oee_metrics", methods=["GET"])
def get_accounts():
    data = fetch_all("oee_metrics")
    return jsonify(data), 200
