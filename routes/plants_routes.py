from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

plants_bp = Blueprint("plants", __name__)

@plants_bp.route("/plants", methods=["GET"])
def get_accounts():
    data = fetch_all("plants")
    return jsonify(data), 200
