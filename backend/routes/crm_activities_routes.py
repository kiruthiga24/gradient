from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import CrmActivities

crm_activities_bp = Blueprint("crm_activities", __name__)

@crm_activities_bp.route("/crm_activities", methods=["GET"])
def get_crm_activities():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(CrmActivities).all()]
    db.close()
    return jsonify(data), 200


@crm_activities_bp.route("/crm_activities", methods=["POST"])
def create_crm_activity():
    db=SessionLocal(); data=request.get_json()
    new_item = CrmActivities(
        account_id=data.get("account_id"),
        signal_id=data.get("signal_id"),
        activity_type=data.get("activity_type"),
        description=data.get("description"),
        due_date=data.get("due_date"),
        status=data.get("status")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201
