from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

rca_analysis_bp = Blueprint("rca_analysis", __name__)

@rca_analysis_bp.route("/rca_analysis", methods=["GET"])
def get_rca_analysis():
    data = fetch_all("rca_analysis")
    return jsonify(data), 200

@rca_analysis_bp.route("/rca_analysis", methods=["POST"])
def create_rca_analysis():
    data = request.json
    created = insert_record("rca_analysis", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

