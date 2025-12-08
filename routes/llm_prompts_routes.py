from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

llm_prompts_bp = Blueprint("llm_prompts", __name__)

@llm_prompts_bp.route("/llm_prompts", methods=["GET"])
def get_llm_prompts():
    data = fetch_all("llm_prompts")
    return jsonify(data), 200

@llm_prompts_bp.route("/llm_prompts", methods=["POST"])
def create_llm_prompts():
    data = request.json
    created = insert_record("llm_prompts", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

