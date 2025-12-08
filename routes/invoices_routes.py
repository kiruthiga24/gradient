from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/invoices", methods=["GET"])
def get_accounts():
    data = fetch_all("invoices")
    return jsonify(data), 200
