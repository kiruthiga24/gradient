from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    data = fetch_all("users")
    return jsonify(data), 200

@users_bp.route("/users", methods=["POST"])
def create_users():
    data = request.json
    created = insert_record("users", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

