from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

churn_risk_assessments_bp = Blueprint("churn_risk_assessments", __name__)

@churn_risk_assessments_bp.route("/churn_risk_assessments", methods=["GET"])
def get_churn_risk_assessments():
    data = fetch_all("churn_risk_assessments")
    return jsonify(data), 200

@churn_risk_assessments_bp.route("/churn_risk_assessments", methods=["POST"])
def create_churn_risk_assessments():
    data = request.json
    created = insert_record("churn_risk_assessments", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

