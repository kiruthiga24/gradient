from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import Accounts
from utils.logger import logger

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/accounts", methods=["GET"])
def get_accounts():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query(Accounts).all()]
    db.close()
    logger.info("Fetching all accounts runs")
    return jsonify(data), 200

