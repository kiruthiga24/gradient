from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

email_drafts_bp = Blueprint("email_drafts", __name__)

@email_drafts_bp.route("/email_drafts", methods=["GET"])
def get_email_drafts():
    data = fetch_all("email_drafts")
    return jsonify(data), 200

@email_drafts_bp.route("/email_drafts", methods=["POST"])
def create_email_drafts():
    data = request.json
    created = insert_record("email_drafts", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

