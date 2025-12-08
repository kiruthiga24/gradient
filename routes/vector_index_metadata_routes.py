from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

vector_index_metadata_bp = Blueprint("vector_index_metadata", __name__)

@vector_index_metadata_bp.route("/vector_index_metadata", methods=["GET"])
def get_vector_index_metadata():
    data = fetch_all("vector_index_metadata")
    return jsonify(data), 200

@vector_index_metadata_bp.route("/vector_index_metadata", methods=["POST"])
def create_vector_index_metadata():
    data = request.json
    created = insert_record("vector_index_metadata", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

