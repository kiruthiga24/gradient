from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Users

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Users).all()]
    db.close()
    return jsonify(data), 200

