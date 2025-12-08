from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    data = fetch_all("customers")
    return jsonify(data), 200

@customers_bp.route("/customers", methods=["POST"])
def create_customers():
    data = request.json
    created = insert_record("customers", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

