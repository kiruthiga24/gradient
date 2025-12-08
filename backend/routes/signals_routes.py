from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Signals

signals_bp = Blueprint("signals", __name__)

@signals_bp.route("/signals", methods=["GET"])
def get_signals():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Signals).all()]
    db.close()
    return jsonify(data), 200

@signals_bp.route("/signals", methods=["POST"])
def create_signal():
    db = SessionLocal()
    data = request.get_json()

    new_item = Signals(
        agent_run_id=data.get("agent_run_id"),
        account_id=data.get("account_id"),
        signal_type=data.get("signal_type"),
        signal_strength=data.get("signal_strength")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()

    return jsonify({"message": "Created", "data": new_item.to_dict()}), 201

