from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Products

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["GET"])
def get_products():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Products).all()]
    db.close()
    return jsonify(data), 200

