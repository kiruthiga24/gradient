from flask import Blueprint, jsonify, request
from utils.create_zoho_crm_actions import *
from utils.logger import logger
from utils.create_zoho_crm_actions import *

crm_bp = Blueprint("crm_actions", __name__)

@crm_bp.route("/crm/push-actions", methods=["POST"])
def push_actions():
    agent_run_id = request.json.get("agent_run_id")

    if not agent_run_id:
        return jsonify({"error": "agent_run_id required"}), 400
    
    zoho_crm = ZohoCRMService()
    success = zoho_crm.push_to_crm(agent_run_id)

    # result = get_recommendations(agent_run_id)
    return jsonify(success), 200
