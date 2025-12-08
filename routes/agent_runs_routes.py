from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

agent_runs_bp = Blueprint("agent_runs", __name__)

@agent_runs_bp.route("/agent_runs", methods=["GET"])
def get_accounts():
    data = fetch_all("agent_runs")
    return jsonify(data), 200
