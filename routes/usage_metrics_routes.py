from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

usage_metrics_bp = Blueprint("usage_metrics", __name__)

@usage_metrics_bp.route("/usage_metrics", methods=["GET"])
def get_usage_metrics():
    data = fetch_all("usage_metrics")
    return jsonify(data), 200

@usage_metrics_bp.route("/usage_metrics", methods=["POST"])
def create_usage_metrics():
    data = request.json
    created = insert_record("usage_metrics", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

