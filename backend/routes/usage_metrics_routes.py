from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import UsageMetrics

usage_metrics_bp = Blueprint("usage_metrics", __name__)

@usage_metrics_bp.route("/usage_metrics", methods=["GET"])
def get_usage_metrics():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(UsageMetrics).all()]
    db.close()
    return jsonify(data), 200

