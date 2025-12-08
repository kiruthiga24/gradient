from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_accounts():
    data = fetch_all("users")
    return jsonify(data), 200
