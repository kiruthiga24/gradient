from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

quality_incidents_bp = Blueprint("quality_incidents", __name__)

@quality_incidents_bp.route("/quality_incidents", methods=["GET"])
def get_quality_incidents():
    data = fetch_all("quality_incidents")
    return jsonify(data), 200

@quality_incidents_bp.route("/quality_incidents", methods=["POST"])
def create_quality_incidents():
    data = request.json
    created = insert_record("quality_incidents", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

