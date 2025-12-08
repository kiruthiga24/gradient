from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

churn_briefs_bp = Blueprint("churn_briefs", __name__)

@churn_briefs_bp.route("/churn_briefs", methods=["GET"])
def get_churn_briefs():
    data = fetch_all("churn_briefs")
    return jsonify(data), 200

@churn_briefs_bp.route("/churn_briefs", methods=["POST"])
def create_churn_briefs():
    data = request.json
    created = insert_record("churn_briefs", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

