from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/accounts", methods=["GET"])
def get_accounts():
    data = fetch_all("accounts")
    return jsonify(data), 200

@accounts_bp.route("/accounts", methods=["POST"])
def create_accounts():
    data = request.json
    created = insert_record("accounts", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

