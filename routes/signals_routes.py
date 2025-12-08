from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

signals_bp = Blueprint("signals", __name__)

@signals_bp.route("/signals", methods=["GET"])
def get_signals():
    data = fetch_all("signals")
    return jsonify(data), 200

@signals_bp.route("/signals", methods=["POST"])
def create_signals():
    data = request.json
    created = insert_record("signals", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

