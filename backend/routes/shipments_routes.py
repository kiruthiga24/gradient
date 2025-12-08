from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Shipments

shipments_bp = Blueprint("shipments", __name__)

@shipments_bp.route("/shipments", methods=["GET"])
def get_shipments():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Shipments).all()]
    db.close()
    return jsonify(data), 200

