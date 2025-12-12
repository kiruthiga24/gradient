from flask import Blueprint, jsonify
from database import SessionLocal
from utils.logger import logger
from models.base_model import LLMSignalPayloads, QualityAction, QualityBrief, QualityEmail, QualityRcaAnalysis
from llm.orchestrator import LLMOrchestrator
import json
from datetime import datetime, timezone


from services.signal_detector.runner import run_all_detectors

console = Blueprint("console", __name__)
llm = LLMOrchestrator()

def clean_indicator(signal_type: str) -> str:
    indicator_map = {
        "order_volume_drop": "Order Drop",
        "usage_decline": "Usage Decline",
        "quality_spike": "Quality Spike",
        "oee_drop": "OEE Drop",
        "support_ticket_spike": "Ticket Spike",
        "shipment_delay_risk": "Shipment Delays",
        "expansion_opportunity": "Expansion Opportunity",
        "qbr_due": "QBR Due"
    }

    return indicator_map.get(
        signal_type,
        signal_type.replace("_", " ").title()   # fallback safe label
    )

def time_ago(created_at):
    # If DB timestamp is naive → make it UTC-aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    diff = now - created_at

    mins = int(diff.total_seconds() / 60)

    if mins < 1:
        return "just now"
    if mins < 60:
        return f"{mins} mins ago"

    hours = mins // 60
    return f"{hours} hrs ago"

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


@console.route("/run/qbr/from-table", methods=["POST"])
def run_qbr():
    db = SessionLocal()

    try:
        logger.info("QBR LLM started successfully")

        row = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "qbr_auto_generation") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .limit(1) \
        .first()


        if not row:
            return jsonify({"error": "No qbr payload found"}), 404
        

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
            use_case="qbr",
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


@console.route("/run/quality/from-table", methods=["POST"])
def run_quality_inc():
    db = SessionLocal()

    try:
        logger.info("Quality LLM started successfully")

        row = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "quality_incident") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .limit(1) \
        .first()


        if not row:
            return jsonify({"error": "No qbr payload found"}), 404
        

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
            use_case="quality_incident",
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


@console.route("/signals/left-pane/<use_case>", methods=["GET"])
def get_left_pane_by_use_case(use_case):

    VALID_CASES = [
        "churn_risk",
        "expansion_opportunity",
        "qbr_auto_generation",
        "supply_risk",
        "quality_incident",
    ]

    if use_case not in VALID_CASES:
        return jsonify({"error": "Invalid use_case"}), 400

    db = SessionLocal()

    rows = (
        db.query(LLMSignalPayloads)
        .filter(LLMSignalPayloads.use_case_name == use_case)
        .order_by(LLMSignalPayloads.created_at.desc())
        .all()
    )

    response = []

    for row in rows:
        data = row.payload_json
        account = data.get("account", {})
        signals = data.get("signals", [])

        indicators = [
            clean_indicator(sig.get("signal_type"))
            for sig in signals
        ]

        response.append({
            "payload_id": str(row.payload_id),
            "agent_run_id": str(row.agent_run_id),
            "account_id": account.get("account_id"),
            "account_name": account.get("account_name"),
            "use_case": row.use_case_name,
            "final_score": row.final_score,
            "risk_level": data.get("risk_level", "N/A"),
            "indicators": indicators,
            "detected_ago": time_ago(row.created_at),
            "created_at": row.created_at.isoformat()
        })

    return jsonify({"data": response})



@console.route("/agent/data/quality/<account_id>/<agent_run_id>", methods=["GET"])
def get_quality_json(account_id, agent_run_id):
    """
    Build final combined JSON for UI middle + right pane.
    """
    db = SessionLocal()

    # ------------------------------
    # 1. FETCH DB ROWS
    # ------------------------------
    rca = (
        db.query(QualityRcaAnalysis)
        .filter_by(agent_run_id=agent_run_id, account_id=account_id)
        .order_by(QualityRcaAnalysis.created_at.desc())
        .first()
    )

    brief = (
        db.query(QualityBrief)
        .filter_by(agent_run_id=agent_run_id, account_id=account_id)
        .order_by(QualityBrief.created_at.desc())
        .first()
    )

    actions = (
        db.query(QualityAction)
        .filter_by(agent_run_id=agent_run_id, account_id=account_id)
        .order_by(QualityAction.created_at.desc())
        .all()
    )

    email = (
        db.query(QualityEmail)
        .filter_by(agent_run_id=agent_run_id, account_id=account_id)
        .order_by(QualityEmail.created_at.desc())
        .first()
    )

    # Safety check
    if not (rca and brief):
        return {"error": "Missing RCA or Brief for this agent_run_id"}

    # ------------------------------
    # 2. FORMAT ACTIONS
    # ------------------------------
    actions_json = [
        {
            "title": act.title,
            "description": act.description,
            "priority": act.priority,
            "assignee_suggestion": act.assignee_suggestion,
            "expected_impact": act.expected_impact,
            "type": act.action_type,
        }
        for act in actions
    ]

    # ------------------------------
    # 3. BUILD FINAL JSON PAYLOAD
    # ------------------------------
    final_json = {
        "use_case": "quality_incident",
        "account_id": account_id,

        # -------- MIDDLE PANE --------
        "brief": {
            "executive_summary": brief.executive_summary,
            "key_findings": brief.key_findings,
            "risk_level": brief.risk_level,
            "impact_estimate": brief.impact_estimate,
            "action_plan": brief.key_findings or []
        },

        "rca": {
            "root_cause_summary": rca.defect_patterns,
            "notes": rca.notes,
            "total_incidents": rca.total_incidents,

            "trends": rca.trends,
            "correlated_factors": rca.correlated_factors,

            # defect patterns → frontend
            "defect_patterns": rca.defect_patterns,
        },

        # -------- RIGHT PANE --------
        "actions": {
            "value": actions_json
        },

        "email": {
            "subject": email.subject if email else None,
            "body": email.body if email else None,
            "to_address": email.to_address if email else None,
        }
    }

    return jsonify({"data": final_json})
