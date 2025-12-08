from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import ChurnRiskAssessments

churn_risk_assessments_bp = Blueprint("churn_risk_assessments", __name__)

@churn_risk_assessments_bp.route("/churn_risk_assessments", methods=["GET"])
def get_churn_risk_assessments():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(ChurnRiskAssessments).all()]
    db.close()
    return jsonify(data), 200

@churn_risk_assessments_bp.route("/churn_risk_assessments", methods=["POST"])
def create_churn_risk_assessment():
    db = SessionLocal()
    data = request.get_json()

    new_item = ChurnRiskAssessments(
        signal_id=data.get("signal_id"),
        account_id=data.get("account_id"),
        risk_score=data.get("risk_score"),
        risk_level=data.get("risk_level")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message": "Created", "data": new_item.to_dict()}), 201
