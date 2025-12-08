from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

quality_incidents_bp = Blueprint("quality_incidents", __name__)

@quality_incidents_bp.route("/quality_incidents", methods=["GET"])
def get_accounts():
    data = fetch_all("quality_incidents")
    return jsonify(data), 200
