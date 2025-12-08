from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Contracts

contracts_bp = Blueprint("contracts", __name__)

@contracts_bp.route("/contracts", methods=["GET"])
def get_contracts():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Contracts).all()]
    db.close()
    return jsonify(data), 200

