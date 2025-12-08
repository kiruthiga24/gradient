from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import RcaAnalysis

rca_analysis_bp = Blueprint("rca_analysis", __name__)

@rca_analysis_bp.route("/rca_analysis", methods=["GET"])
def get_rca_analysis():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(RcaAnalysis).all()]
    db.close()
    return jsonify(data), 200

@rca_analysis_bp.route("/rca_analysis", methods=["POST"])
def create_rca():
    db = SessionLocal()
    data = request.get_json()

    new_item = RcaAnalysis(
        signal_id=data.get("signal_id"),
        root_causes=data.get("root_causes"),
        confidence_score=data.get("confidence_score")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()

    return jsonify({"message": "Created", "data": new_item.to_dict()}), 201
