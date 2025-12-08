from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

contracts_bp = Blueprint("contracts", __name__)

@contracts_bp.route("/contracts", methods=["GET"])
def get_contracts():
    data = fetch_all("contracts")
    return jsonify(data), 200

@contracts_bp.route("/contracts", methods=["POST"])
def create_contracts():
    data = request.json
    created = insert_record("contracts", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

