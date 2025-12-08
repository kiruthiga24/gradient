from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import QualityIncidents

quality_incidents_bp = Blueprint("quality_incidents", __name__)

@quality_incidents_bp.route("/quality_incidents", methods=["GET"])
def get_quality_incidents():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(QualityIncidents).all()]
    db.close()
    return jsonify(data), 200

