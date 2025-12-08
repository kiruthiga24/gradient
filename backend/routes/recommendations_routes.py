from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Recommendations

recommendations_bp = Blueprint("recommendations", __name__)

@recommendations_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Recommendations).all()]
    db.close()
    return jsonify(data), 200


@recommendations_bp.route("/recommendations", methods=["POST"])
def create_recommendation():
    db=SessionLocal(); data=request.get_json()
    new_item = Recommendations(
        signal_id=data.get("signal_id"),
        account_id=data.get("account_id"),
        action_type=data.get("action_type"),
        action_details=data.get("action_details"),
        priority=data.get("priority")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201
