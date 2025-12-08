from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import ChurnBriefs

churn_briefs_bp = Blueprint("churn_briefs", __name__)

@churn_briefs_bp.route("/churn_briefs", methods=["GET"])
def get_churn_briefs():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(ChurnBriefs).all()]
    db.close()
    return jsonify(data), 200


@churn_briefs_bp.route("/churn_briefs", methods=["POST"])
def create_churn_brief():
    db = SessionLocal(); data = request.get_json()
    new_item = ChurnBriefs(
        signal_id=data.get("signal_id"),
        account_id=data.get("account_id"),
        brief_text=data.get("brief_text")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201
