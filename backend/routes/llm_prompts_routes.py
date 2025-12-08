from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import LlmPrompts

llm_prompts_bp = Blueprint("llm_prompts", __name__)

@llm_prompts_bp.route("/llm_prompts", methods=["GET"])
def get_llm_prompts():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(LlmPrompts).all()]
    db.close()
    return jsonify(data), 200

@llm_prompts_bp.route("/llm_prompts", methods=["POST"])
def create_prompt():
    db=SessionLocal(); data=request.get_json()
    new_item = LlmPrompts(
        prompt_name=data.get("prompt_name"),
        prompt_template=data.get("prompt_template"),
        version=data.get("version")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201

