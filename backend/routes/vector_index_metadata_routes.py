from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import VectorIndexMetadata

vector_index_metadata_bp = Blueprint("vector_index_metadata", __name__)

@vector_index_metadata_bp.route("/vector_index_metadata", methods=["GET"])
def get_vector_index_metadata():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(VectorIndexMetadata).all()]
    db.close()
    return jsonify(data), 200

@vector_index_metadata_bp.route("/vector_index_metadata",methods=["POST"])
def create_vector_meta():
    db=SessionLocal(); data=request.get_json()
    new_item = VectorIndexMetadata(
        entity_type=data.get("entity_type"),
        entity_id=data.get("entity_id"),
        embedding_model=data.get("embedding_model")
    )
    db.add(new_item); db.commit(); db.refresh(new_item); db.close()
    return jsonify({"message":"Created","data":new_item.to_dict()}),201

