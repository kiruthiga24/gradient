from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Invoices

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/invoices", methods=["GET"])
def get_invoices():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Invoices).all()]
    db.close()
    return jsonify(data), 200

