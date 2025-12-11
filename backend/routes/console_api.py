from flask import Blueprint, jsonify, request
from database import SessionLocal
from utils.logger import logger

from services.signal_detector.runner import run_all_detectors
# from services.crm.zoho_sender import send_email_to_zoho
from services.email.email_sender import send_email
from models.base_model import EmailDrafts
from services.crm.zoho_sender import create_zoho_crm_task

console = Blueprint("console", __name__)

@console.route("/signals/run", methods=["POST"])
def run_signals():
    db = SessionLocal()

    try:
        logger.info("Signal detection started successfully")
        result = run_all_detectors(db)
        logger.info("Signal detection completed successfully")

        return jsonify({
            "status": "success",
            "signals_generated": result["total_signals"],
            "agent_run_id": result["agent_run_id"]
        }), 200

    except Exception as e:
        logger.error(f"Signal detection failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.close()

@console.route("/email/send", methods=["POST"])
def send_email_route():
    """
    Send an email using a draft from the database.
    POST JSON body:
    {
        "email_id": "UUID of the draft you want to send"
    }
    """
    db = SessionLocal()
    data = request.get_json()
    email_id = data.get("email_id")

    #my email
    from_email = "sunil@saturam.com"

    if not email_id:
        return jsonify({"status": "error", "message": "Missing email_id"}), 400

    # Fetch draft from DB
    draft = db.query(EmailDrafts).filter(EmailDrafts.email_id == email_id).first()
    if not draft:
        db.close()
        return jsonify({"status": "error", "message": "Draft not found"}), 404

    # Send email using SMTP_USER from email_sender.py
    success = send_email(
        from_email,
        to_email=draft.to_email,
        subject=draft.subject,
        body_text=draft.body_text
    )

    # db.close()

    # if success:
    #     return jsonify({"status": "success", "message": f"Email sent to {draft.to_email}"}), 200
    # else:
    #     return jsonify({"status": "error", "message": "Failed to send email"}), 500

    if not success:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500

    crm_result = create_zoho_crm_task(
        subject=f"Follow-up Email Sent: {draft.subject}",
        description=draft.body_text
    )

    if not crm_result:
        return jsonify({"status": "error", "message": "Email sent but failed to create Zoho task"}), 500

    return jsonify({
        "status": "success",
        "message": "Email sent and Zoho CRM task created",
        "zoho_response": crm_result
    }), 200

# @console.route("/crm/send-email", methods=["POST"])
# def crm_send_email():
#     db = SessionLocal()

#     try:
#         data = request.get_json()
#         email_id = data.get("email_id")

#         if not email_id:
#             return jsonify({"status": "error", "message": "email_id is required"}), 400

#         logger.info(f"CRM Email sending started for email_id: {email_id}")

#         result = send_email_to_zoho(db, email_id)

#         logger.info("CRM Email sent successfully")

#         return jsonify({
#             "status": "success",
#             "zoho_response": result
#         }), 200

#     except Exception as e:
#         logger.error(f"CRM email send failed: {str(e)}")
#         return jsonify({"status": "error", "message": str(e)}), 500

#     finally:
#         db.close()