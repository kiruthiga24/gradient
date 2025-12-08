from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import SupportTickets

support_tickets_bp = Blueprint("support_tickets", __name__)

@support_tickets_bp.route("/support_tickets", methods=["GET"])
def get_support_tickets():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(SupportTickets).all()]
    db.close()
    return jsonify(data), 200

