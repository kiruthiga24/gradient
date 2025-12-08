from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

agent_runs_bp = Blueprint("agent_runs", __name__)

@agent_runs_bp.route("/agent_runs", methods=["GET"])
def get_agent_runs():
    data = fetch_all("agent_runs")
    return jsonify(data), 200

@agent_runs_bp.route("/agent_runs", methods=["POST"])
def create_agent_runs():
    data = request.json
    created = insert_record("agent_runs", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

