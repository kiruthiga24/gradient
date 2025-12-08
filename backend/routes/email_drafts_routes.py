from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import EmailDrafts

email_drafts_bp = Blueprint("email_drafts", __name__)

@email_drafts_bp.route("/email_drafts", methods=["GET"])
def get_email_drafts():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(EmailDrafts).all()]
    db.close()
    return jsonify(data), 200

@email_drafts_bp.route("/email_drafts",methods=["POST"])
def create_email_draft():
    db=SessionLocal(); data=request.get_json()
    new_item = EmailDrafts(
        signal_id=data.get("signal_id"),
        to_email=data.get("to_email"),
        subject=data.get("subject"),
        body_text=data.get("body_text")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201

