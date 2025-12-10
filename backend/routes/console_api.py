from flask import Blueprint, jsonify
from database import SessionLocal
from utils.logger import logger
from models.base_model import LLMSignalPayloads
from llm.orchestrator import LLMOrchestrator
import json

from services.signal_detector.runner import run_all_detectors

console = Blueprint("console", __name__)
llm = LLMOrchestrator()

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

@console.route("/run/expansion/from-table", methods=["POST"])
def run_expansion():
    db = SessionLocal()

    try:
        logger.info("Expansion LLM started successfully")

        row = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "expansion_opportunity") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .limit(1) \
        .first()


        if not row:
            return jsonify({"error": "No expansion payload found"}), 404
        

        print("*********")
        print("Row", row)

        payload_id = row.payload_id
        score = row.final_score
        agent_run_id = row.agent_run_id
        print(agent_run_id)
        payload_json = row.payload_json
        payload = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        payload["payload_id"] = str(payload_id)
        payload["final_score"] = score

        print("Payload", payload)

        # Call orchestrator
        result = llm.run_pipeline(
            db,
            use_case="expansion",
            payload=payload,
            agent_run_id=agent_run_id
        )

        return jsonify({
            "payload_id": str(payload_id),
            "status": "processed",
            "llm_output": result
        })

    except Exception as e:
        logger.error(f"Signal detection failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.close()
