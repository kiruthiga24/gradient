from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/invoices", methods=["GET"])
def get_invoices():
    data = fetch_all("invoices")
    return jsonify(data), 200

@invoices_bp.route("/invoices", methods=["POST"])
def create_invoices():
    data = request.json
    created = insert_record("invoices", data)
    return jsonify({"status": "success", "inserted": created}), 201
    

