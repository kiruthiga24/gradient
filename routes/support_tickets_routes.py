from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

support_tickets_bp = Blueprint("support_tickets", __name__)

@support_tickets_bp.route("/support_tickets", methods=["GET"])
def get_support_tickets():
    data = fetch_all("support_tickets")
    return jsonify(data), 200

@support_tickets_bp.route("/support_tickets", methods=["POST"])
def create_support_tickets():
    data = request.json
    created = insert_record("support_tickets", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

