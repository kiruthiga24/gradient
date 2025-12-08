from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Customers

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Customers).all()]
    db.close()
    return jsonify(data), 200

