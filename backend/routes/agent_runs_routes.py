from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import AgentRuns

agent_runs_bp = Blueprint("agent_runs", __name__)

@agent_runs_bp.route("/agent_runs", methods=["GET"])
def get_agent_runs():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(AgentRuns).all()]
    db.close()
    return jsonify(data), 200

@agent_runs_bp.route("/agent_runs", methods=["POST"])
def create_agent_run():
    db = SessionLocal()
    data = request.get_json()

    new_run = AgentRuns(
        run_type=data.get("run_type"),
        status=data.get("status")
    )

    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    db.close()

    return jsonify({
        "message": "Agent Run created successfully",
        "data": new_run.to_dict()
    }), 201
