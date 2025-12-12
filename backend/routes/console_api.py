from flask import Blueprint, jsonify
from database import SessionLocal
from utils.logger import logger
from models.base_model import LLMSignalPayloads, QualityAction, QualityBrief, QualityEmail, QualityRcaAnalysis, ExpansionBrief, ExpansionDeck, ExpansionRcaAnalysis, ExpansionRecommendation, ExpansionRevenueEstimate
from llm.orchestrator import LLMOrchestrator
import json
from datetime import datetime, timezone

from decimal import Decimal

def to_json_safe(obj):
    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_safe(v) for v in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

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

@console.route("/run/churn-risk", methods=["POST"])
def run_churn():
    db = SessionLocal()

    try:
        logger.info("Expansion LLM started successfully")

        row = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "churn_risk") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .limit(1) \
        .first()


        if not row:
            return jsonify({"error": "No Churn payload found"}), 404
        

        print("*********")
        print("Row", row)

        payload_id = row.payload_id
        score = row.final_score
        agent_run_id = row.agent_run_id
        print(agent_run_id)
        payload_json = row.payload_json
        payload_raw = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        payload = to_json_safe(payload_raw)
        payload["payload_id"] = str(payload_id)
        payload["final_score"] = float(score) if isinstance(score, Decimal) else score
        print("Payload", payload)

        # Call orchestrator
        result = llm.run_pipeline(
            db,
            use_case="churn_risk",
            payload=payload,
            agent_run_id=agent_run_id
        )

        return jsonify({
            "payload_id": str(payload_id),
            "status": "processed",
            "llm_output": result
        })

    except Exception as e:
        logger.error(f"Churn Run failed: {str(e)}")
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
    except Exception as e:
        logger.error(f"Signal detection failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
        

@console.route("/run/supply-risk", methods=["POST"])
def run_supply_risk():
    db = SessionLocal()
    try:
        row = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "supply_risk") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .limit(1) \
        .first()
        if not row:
            return jsonify({"message": "No supply risk records"}), 404
        
        print("*********")
        print("Row", row)

        payload_id = row.payload_id
        score = row.final_score
        agent_run_id = row.agent_run_id
        payload_json = row.payload_json
        payload = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        payload["payload_id"] = str(payload_id)
        payload["final_score"] = score
        payload_raw = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        payload = to_json_safe(payload_raw)
               
        print("Payload", payload)

        # Call orchestrator
        result = llm.run_pipeline(
            db,
            use_case="supply_risk",
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
        logger.error(f"Churn Run failed: {str(e)}")
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

    db.close()
    return jsonify({"data": response})



@console.route("/agent/data/quality_incident/<account_id>/<agent_run_id>", methods=["GET"])
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
    db.close()

    return jsonify({"data": final_json})

@console.route("/agent/data/expansion_opportunity/<account_id>/<agent_run_id>", methods=["GET"])
def get_expansion_json(account_id, agent_run_id):
    session = SessionLocal()
    # 2. Fetch all tables for this run
    rca = (
        session.query(ExpansionRcaAnalysis)
        .filter_by(account_id=account_id, agent_run_id=agent_run_id)
        .first()
    )

    brief = (
        session.query(ExpansionBrief)
        .filter_by(account_id=account_id, agent_run_id=agent_run_id)
        .first()
    )

    revenue = (
        session.query(ExpansionRevenueEstimate)
        .filter_by(account_id=account_id, agent_run_id=agent_run_id)
        .first()
    )

    actions = (
        session.query(ExpansionRecommendation)
        .filter_by(account_id=account_id, agent_run_id=agent_run_id)
        .order_by(ExpansionRecommendation.priority)
        .all()
    )

    deck = (
        session.query(ExpansionDeck)
        .filter_by(account_id=account_id, agent_run_id=agent_run_id)
        .first()
    )

    # 3. Derive "primary signal", "competitor risk", etc
    primary_signal = None
    competitor_risk = None
    estimated_upside = None
    signal_confidence = None

    if rca and rca.usage_anomalies:
        top = rca.usage_anomalies[0]
        primary_signal = top.get("pattern", "")
        signal_confidence = top.get("confidence", 0)

    if rca and rca.competitor_dependency:
        c = rca.competitor_dependency[0]
        competitor_risk = f"Dependency on {c.get('their_sku', '')}"

    if revenue:
        estimated_upside = float(revenue.estimated_monthly_revenue)

    # 4. Build UI JSON
    ui_json = {
        "middle_panel": {
            "executive_summary": brief.brief_summary if brief else "",
            "primary_signal": primary_signal,
            "competitor_risk": competitor_risk,
            "estimated_upside": estimated_upside,
            "signal_confidence": signal_confidence,

            "detected_signals": {
                "usage_anomalies": rca.usage_anomalies if rca else [],
                "competitor_dependency": rca.competitor_dependency if rca else [],
                "bom_gaps": rca.bom_gaps if rca else []
            },

            "commercial_intelligence": {
                "brief_summary": brief.brief_summary if brief else "",
                "commercial_insight": brief.whitespace_opportunities if brief else "",
                "detected_patterns": brief.cross_sell_targets if brief else []
            },

            "revenue_opportunity": {
                "currency": revenue.currency if revenue else "",
                "estimated_monthly_revenue": float(revenue.estimated_monthly_revenue) if revenue else None,
                "estimated_annual_revenue": float(revenue.estimated_annual_revenue) if revenue else None,
                "assumptions": revenue.assumptions if revenue else [],
                "revenue_model":[]  # if you want table view, fill from RCA or transformed data
            }
        },

        "right_panel": {
            "actions": [
                {
                    "priority": a.priority,
                    "type": a.recommendation_type,
                    "target_sku": a.target_sku,
                    "rationale": a.rationale,
                    "expected_lift": float(a.expected_lift) if a.expected_lift else None
                }
                for a in actions
            ],
            "deck": {
                "deck_title": deck.deck_title if deck else "",
                "slides": deck.deck_outline if deck else []
            }
        }
    }

    session.close()

    return jsonify({"data": ui_json})
