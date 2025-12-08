from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

recommendations_bp = Blueprint("recommendations", __name__)

@recommendations_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    data = fetch_all("recommendations")
    return jsonify(data), 200

@recommendations_bp.route("/recommendations", methods=["POST"])
def create_recommendations():
    data = request.json
    created = insert_record("recommendations", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

