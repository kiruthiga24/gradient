from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Plants

plants_bp = Blueprint("plants", __name__)

@plants_bp.route("/plants", methods=["GET"])
def get_plants():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Plants).all()]
    db.close()
    return jsonify(data), 200

