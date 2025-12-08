from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["GET"])
def get_products():
    data = fetch_all("products")
    return jsonify(data), 200

@products_bp.route("/products", methods=["POST"])
def create_products():
    data = request.json
    created = insert_record("products", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

