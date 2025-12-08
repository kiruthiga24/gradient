from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import AgentMemory

agent_memory_bp = Blueprint("agent_memory", __name__)

@agent_memory_bp.route("/agent_memory", methods=["GET"])
def get_agent_memory():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(AgentMemory).all()]
    db.close()
    return jsonify(data), 200


@agent_memory_bp.route("/agent_memory", methods=["POST"])
def create_agent_memory():
    db=SessionLocal(); data=request.get_json()
    new_item = AgentMemory(
        agent_run_id=data.get("agent_run_id"),
        memory_type=data.get("memory_type"),
        memory_payload=data.get("memory_payload")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201
