from flask import Blueprint, jsonify, request
from database import SessionLocal
from utils.logger import logger

from services.signal_detector.runner import run_all_detectors
from services.crm.zoho_sender import send_email_to_zoho

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


@console.route("/crm/send-email", methods=["POST"])
def crm_send_email():
    db = SessionLocal()

    try:
        data = request.get_json()
        email_id = data.get("email_id")

        if not email_id:
            return jsonify({"status": "error", "message": "email_id is required"}), 400

        logger.info(f"CRM Email sending started for email_id: {email_id}")

        result = send_email_to_zoho(db, email_id)

        logger.info("CRM Email sent successfully")

        return jsonify({
            "status": "success",
            "zoho_response": result
        }), 200

    except Exception as e:
        logger.error(f"CRM email send failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.close()