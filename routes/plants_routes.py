from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

plants_bp = Blueprint("plants", __name__)

@plants_bp.route("/plants", methods=["GET"])
def get_plants():
    data = fetch_all("plants")
    return jsonify(data), 200

@plants_bp.route("/plants", methods=["POST"])
def create_plants():
    data = request.json
    created = insert_record("plants", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

