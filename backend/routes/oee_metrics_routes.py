from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import OeeMetrics

oee_metrics_bp = Blueprint("oee_metrics", __name__)

@oee_metrics_bp.route("/oee_metrics", methods=["GET"])
def get_oee_metrics():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(OeeMetrics).all()]
    db.close()
    return jsonify(data), 200

