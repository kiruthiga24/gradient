from flask import Blueprint, jsonify, send_file, request
from utils.create_zoho_crm_actions import *
from utils.logger import logger
from utils.create_zoho_crm_actions import *
import os

crm_bp = Blueprint("crm_actions", __name__)

@crm_bp.route("/agent/action/create-tasks", methods=["POST"])
@crm_bp.route("/agent/action/create-crm-task", methods=["POST"])
def push_actions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # agent_run_id = request.json.get("agent_run_id")
    # agent_run_id = data.get("agent_run_id")

    # if not agent_run_id:
    #     return jsonify({"error": "agent_run_id required"}), 400

    zoho_crm = ZohoCRMService()
    result = zoho_crm.push_to_crm(data)

    # result = get_recommendations(agent_run_id)
    return jsonify(result), 200

@crm_bp.route("/agent/action/download-brief", methods=["POST"])
def download_brief():
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "Invalid JSON body"}), 400

    if "brief" not in payload:
        return jsonify({"error": "brief content is required"}), 400

    logger.info(
        f"Generating brief PDF | agent_run_id={payload.get('agent_run_id')}"
    )

    os.makedirs("generated_briefs", exist_ok=True)

    file_name = f"brief_{uuid.uuid4()}.pdf"
    file_path = os.path.join("generated_briefs", file_name)

    pdf_generator = Pdf_generator()
    pdf_generator.generate_brief_pdf(payload, file_path)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="Account_Action_Brief.pdf",
        mimetype="application/pdf"
    )


@crm_bp.route("/agent/action/send-email", methods=["POST"])
def send_apology_email():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    required_fields = ["to", "subject", "body", "account_id", "agent_run_id"]
    missing = [f for f in required_fields if not data.get(f)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    email_service = EmailService()

    try:
        email_id = email_service.send_email(
            to_email=data["to"],
            subject=data["subject"],
            body=data["body"]
        )

        # Optional: store audit in DB here (agent_run_id, account_id, email_id)

        return jsonify({
            "success": True,
            "message": "Email sent successfully",
            "email_id": email_id
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "message": "Failed to send email"
        }), 500
    

@crm_bp.route("/agent/run-analysis/<use_case>", methods=["POST"])
def run_analysis(use_case):

    logger.info(
        f"Inside run analysis: {use_case}"
    )
    resp = requests.post(
        f"http://127.0.0.1:5000/signals/run",
        timeout=5
    )
    health = resp.json()

    usecase_url = {
        "churn_risk": "http://127.0.0.1:5000/run/churn-risk",
        "expansion_opportunity": "http://127.0.0.1:5000/run/expansion/from-table",
        "quality_incident": "http://127.0.0.1:5000/run/quality/from-table",
        "qbr_auto_generation": "http://127.0.0.1:5000/run/qbr/from-table",
        "supply_risk": "http://127.0.0.1:5000/run/supply-risk"
    }

    resp = requests.post(
        usecase_url[use_case],
        timeout=5
    )
    health = resp.json()

    return jsonify({
        "health": health
    }), 200
    

    
