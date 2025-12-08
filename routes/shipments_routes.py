from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

shipments_bp = Blueprint("shipments", __name__)

@shipments_bp.route("/shipments", methods=["GET"])
def get_shipments():
    data = fetch_all("shipments")
    return jsonify(data), 200

@shipments_bp.route("/shipments", methods=["POST"])
def create_shipments():
    data = request.json
    created = insert_record("shipments", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

