from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

oee_metrics_bp = Blueprint("oee_metrics", __name__)

@oee_metrics_bp.route("/oee_metrics", methods=["GET"])
def get_oee_metrics():
    data = fetch_all("oee_metrics")
    return jsonify(data), 200

@oee_metrics_bp.route("/oee_metrics", methods=["POST"])
def create_oee_metrics():
    data = request.json
    created = insert_record("oee_metrics", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

