from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

support_tickets_bp = Blueprint("support_tickets", __name__)

@support_tickets_bp.route("/support_tickets", methods=["GET"])
def get_accounts():
    data = fetch_all("support_tickets")
    return jsonify(data), 200
