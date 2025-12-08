from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

agent_memory_bp = Blueprint("agent_memory", __name__)

@agent_memory_bp.route("/agent_memory", methods=["GET"])
def get_agent_memory():
    data = fetch_all("agent_memory")
    return jsonify(data), 200

@agent_memory_bp.route("/agent_memory", methods=["POST"])
def create_agent_memory():
    data = request.json
    created = insert_record("agent_memory", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

