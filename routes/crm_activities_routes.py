from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

crm_activities_bp = Blueprint("crm_activities", __name__)

@crm_activities_bp.route("/crm_activities", methods=["GET"])
def get_crm_activities():
    data = fetch_all("crm_activities")
    return jsonify(data), 200

@crm_activities_bp.route("/crm_activities", methods=["POST"])
def create_crm_activities():
    data = request.json
    created = insert_record("crm_activities", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

