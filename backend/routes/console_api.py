from flask import Blueprint, jsonify
from database import SessionLocal
from utils.logger import logger
from models.base_model import LLMSignalPayloads, RcaAnalysis, ChurnBriefs, QualityAction, QualityBrief, QualityEmail, QualityRcaAnalysis,\
    Recommendations, EmailDrafts, SupplyRca, SupplyBrief, SupplyAction, SupplyEmail, QbrAction, QbrDeck, QbrRcaAnalysis, QbrTalkingPoints, \
    QbrOpportunity, QbrBrief
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

        rows = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "churn_risk") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .all()


        if not rows:
            return jsonify({"error": "No Churn payload found"}), 404
        

        print("*********")
        print("Row", rows)

        responses = []
        for row in rows:
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

            responses.append({
                "payload_id": str(payload_id),
                "agent_run_id": str(agent_run_id),
                "llm_output": to_json_safe(result)  # Ensure JSON serializable
            })

        return jsonify({
            "status": "processed",
            "records_processed": len(responses),
            "results": responses
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

        rows = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "expansion_opportunity") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .all()


        if not rows:
            return jsonify({"error": "No expansion payload found"}), 404
        

        responses = []
        print("*********")
        print("Row", rows)

        for row in rows:
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
                use_case="qbr",
                payload=payload,
                agent_run_id=agent_run_id
            )

            responses.append({
                "payload_id": str(payload_id),
                "agent_run_id": str(agent_run_id),
                "llm_output": to_json_safe(result)  # Ensure JSON serializable
            })

        return jsonify({
            "status": "processed",
            "records_processed": len(responses),
            "results": responses
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

        rows = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "qbr_auto_generation") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .all()


        if not rows:
            return jsonify({"error": "No qbr payload found"}), 404
        

        print("*********")
        print("Row", rows)
        
        responses = []
        for row in rows:
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
                use_case="qbr",
                payload=payload,
                agent_run_id=agent_run_id
            )

            responses.append({
                "payload_id": str(payload_id),
                "agent_run_id": str(agent_run_id),
                "llm_output": to_json_safe(result)  # Ensure JSON serializable
            })

        return jsonify({
            "status": "processed",
            "records_processed": len(responses),
            "results": responses
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

        rows = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "quality_incident") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .all()

        if not rows:
            return jsonify({"error": "No qbr payload found"}), 404
        
        print("*********")
        print("Row", rows)

        responses = []
        for row in rows:
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
                use_case="quality_incident",
                payload=payload,
                agent_run_id=agent_run_id
            )

            responses.append({
                "payload_id": str(payload_id),
                "agent_run_id": str(agent_run_id),
                "llm_output": to_json_safe(result)  # Ensure JSON serializable
            })

        return jsonify({
            "status": "processed",
            "records_processed": len(responses),
            "results": responses
        })

    except Exception as e:
        logger.error(f"Signal detection failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
        

@console.route("/run/supply-risk", methods=["POST"])
def run_supply_risk():
    db = SessionLocal()
    try:
        rows = db.query(LLMSignalPayloads) \
        .filter(LLMSignalPayloads.use_case_name == "supply_risk") \
        .order_by(LLMSignalPayloads.created_at.desc()) \
        .all()
        if not rows:
            return jsonify({"message": "No supply risk records"}), 404
        
        print("*********")
        print("Row", rows)

        responses = []

        for row in rows:
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
                use_case="supply_risk",
                payload=payload,
                agent_run_id=agent_run_id
            )

            responses.append({
                "payload_id": str(payload_id),
                "agent_run_id": str(agent_run_id),
                "llm_output": to_json_safe(result)  # Ensure JSON serializable
            })

        return jsonify({
            "status": "processed",
            "records_processed": len(responses),
            "results": responses
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
    return jsonify({"data": response})

@console.route("/churn-risk/middle_pane/<agent_run_id>/<account_id>", methods=["GET"])
def get_churn_middle_pane(agent_run_id, account_id):

    # FETCH RCA
    # -------------------------------
    db  = SessionLocal()    
    rca_row = (db.query(RcaAnalysis). \
                filter( RcaAnalysis.agent_run_id == agent_run_id,
                        RcaAnalysis.account_id == account_id)). \
                order_by(RcaAnalysis.created_at.desc()).\
                first()

    if not rca_row:
        raise Exception("No RCA found")
    # -------------------------------
    # FETCH BRIEF
    # -------------------------------
    brief_row = (db.query(ChurnBriefs). \
                filter( ChurnBriefs.agent_run_id == agent_run_id,
                        ChurnBriefs.account_id == account_id)). \
                order_by(ChurnBriefs.created_at.desc()). \
                first()
    if not brief_row:
        raise Exception("No Brief found")
    # -------------------------------
    # FETCH ACTIONS
    # -------------------------------

    actions_raw = (
            db.query(Recommendations)
            .filter(
                Recommendations.agent_run_id == agent_run_id,
                Recommendations.account_id == account_id
            )
            .order_by(Recommendations.created_at.desc())
            .all()
        )
    if not actions_raw:
        raise Exception("No Actions found")  
     # ------------------------------------------
        # FETCH EMAIL (Right Pane)
        # ------------------------------------------
    email_raw = (
            db.query(EmailDrafts)
            .filter(
                EmailDrafts.agent_run_id == agent_run_id,
                EmailDrafts.account_id == account_id
            )
            .order_by(EmailDrafts.created_at.desc())
            .first()
        )

    # Build UI JSON response
    response = {
            "risk_summary": {
            "primary_driver": rca_row.root_causes[0].get("cause") if rca_row.root_causes else "",
            "risk_level": rca_row.severity,
            "estimated_impact": rca_row.business_impact,
            "confidence_score": rca_row.confidence_score,
            "executive_summary": brief_row.exec_summary
            },

            "detected_root_causes": [
            {
                "title": f"Root Cause {idx + 1}",
                "cause": rc.get("cause", ""),
                "confidence": rc.get("confidence", "")
            }
            for idx, rc in enumerate(rca_row.root_causes)
             ],

            "commercial_brief": {
            "title": brief_row.title,
            "executive_summary": brief_row.exec_summary,
            "key_drivers": brief_row.key_drivers,
            "recommended_focus": brief_row.recommended_focus
            },

            "actions": [
            {
                        "action": a.action_details,
                        "owner": a.owner,
                        "due_date": a.due_date,
                        "priority": a.priority
            }
            for a in actions_raw
            ],
            
        "email_draft": {
                    "subject": email_raw.subject if email_raw else "",
                    "body_text": email_raw.body_text if email_raw else ""
                }
            }
    
    db.close()
    return response




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

@console.route("/supply_risk/ui/<agent_run_id>/<account_id>", methods=["GET"])
def get_supply_ui_json(agent_run_id, account_id):

    db= SessionLocal()

    # 1️⃣ Fetch RCA
    rca_raw = (db.query(SupplyRca). \
                filter( SupplyRca.agent_run_id == agent_run_id,
                        SupplyRca.account_id == account_id). \
                order_by(SupplyRca.created_at.desc()).\
                first())


    # 2️⃣ Fetch Brief
    brief_raw = (db.query(SupplyBrief). \
            filter(SupplyBrief.agent_run_id==agent_run_id,
                    SupplyBrief.account_id==account_id). \
            order_by(SupplyBrief.created_at.desc()). \
            first())

    # 3️⃣ Fetch Actions
    actions_raw = (db.query(SupplyAction). \
                filter(SupplyAction.agent_run_id==agent_run_id,
                           SupplyAction.account_id==account_id). \
                order_by(SupplyAction.created_at.desc()). \
                all())

    # 4️⃣ Fetch Email
    email_raw= (db.query(SupplyEmail). \
            filter(SupplyEmail.agent_run_id==agent_run_id, 
                   SupplyEmail.account_id==account_id). \
            order_by(SupplyEmail.created_at.desc()). \
            first())
    
    actions_list = []
    for a in actions_raw:
        # Immediate Actions
        if a.immediate_action:
            for act in a.immediate_action:
                actions_list.append({
                    "action": act.get("action", ""),
                    "owner": act.get("owner", ""),
                    "due_date": act.get("due", None),
                    "priority": act.get("priority", "Medium")
                })
        # Follow-up Actions
        if a.follow_up_action:
            for act in a.follow_up_action:
                actions_list.append({
                    "action": act.get("action", ""),
                    "owner": act.get("owner", ""),
                    "due_date": act.get("due", None),
                    "priority": act.get("priority", "Medium")
                })

    result = {
            "risk_summary": {
                "primary_driver": rca_raw.root_causes[0]["cause"] if rca_raw and rca_raw.root_causes else "",
                "risk_level": rca_raw.severity if rca_raw else "",
                "estimated_impact": rca_raw.business_impact if rca_raw else "",
                "confidence_score": float(rca_raw.confidence_score) if rca_raw and rca_raw.confidence_score else 0.0,
                "executive_summary": brief_raw.situation if brief_raw else ""
            },
            "detected_root_causes": [
                {
                    "cause": cause.get("cause", "N/A"),
                    "confidence": float(cause.get("confidence", 0.0))
                }
                for cause in rca_raw.root_causes
            ] if rca_raw and rca_raw.root_causes else [],
            "commercial_brief": {
                "title": "Supply Risk Brief",
                "executive_summary": brief_raw.situation if brief_raw and brief_raw.situation else "N/A",
                "key_drivers": [
                    brief_raw.key_metrics.get("primary_risk", "")
                ] if brief_raw and brief_raw.key_metrics else [],
                "recommended_focus": brief_raw.key_metrics.get("revenue_impact", "") if brief_raw and brief_raw.key_metrics else ""
        },
        
            "actions": actions_list,
            "email": {
                "subject": email_raw.subject if email_raw and email_raw.subject else "",
                "body_text": email_raw.body_text if email_raw and email_raw.body_text else ""
        }
    
    }
    db.close()
    return jsonify(result)

@console.route("/qbr/ui/<account_id>", methods=["GET"])
@console.route("/qbr/ui/<account_id>/<agent_run_id>", methods=["GET"])
def get_qbr_ui_json(account_id, agent_run_id=None):
    db = SessionLocal()

    try:
        # 1️⃣ Determine latest agent_run_id if not provided
       
        rca = (
            db.query(QbrRcaAnalysis)
            .filter(QbrRcaAnalysis.account_id == account_id, QbrRcaAnalysis.agent_run_id == agent_run_id)
            .first()
        )

        brief = (
            db.query(QbrBrief)
            .filter(QbrBrief.account_id == account_id, QbrBrief.agent_run_id == agent_run_id)
            .first()
        )

        opportunities = (
            db.query(QbrOpportunity)
            .filter(QbrOpportunity.account_id == account_id, QbrOpportunity.agent_run_id == agent_run_id)
            .all()
        )

        actions = (
            db.query(QbrAction)
            .filter(QbrAction.account_id == account_id, QbrAction.agent_run_id == agent_run_id)
            .all()
        )

        deck = (
            db.query(QbrDeck)
            .filter(QbrDeck.account_id == account_id, QbrDeck.agent_run_id == agent_run_id)
            .first()
        )

        talking_points = (
            db.query(QbrTalkingPoints)
            .filter(QbrTalkingPoints.account_id == account_id, QbrTalkingPoints.agent_run_id == agent_run_id)
            .first()
        )

        # 3️⃣ Build final JSON
        ui_json = {
            
                "trends": rca.trends if rca and rca.trends else {"orders": 0, "usage": 0, "quality": 0, "tickets": 0},
                "root_causes": rca.root_causes if rca and rca.root_causes else [],
                "signals": rca.signals if rca and rca.signals else {"wins": [], "risks": [], "opportunities": []},
                "brief": {
                    "executive_summary": brief.executive_summary if brief else "",
                    "key_wins": brief.key_wins if brief and brief.key_wins else [],
                    "key_risks": brief.key_risks if brief and brief.key_risks else [],
                    "opportunities_summary": brief.opportunities_summary if brief and brief.opportunities_summary else []
                },
                "opportunities": [
                    {
                        "type": o.type or "",
                        "sku": o.sku or "",
                        "rationale": o.rationale or "",
                        "estimated_value": float(o.estimated_value) if o.estimated_value is not None else 0
                    } for o in opportunities
                ],
                "actions": [
                    {
                        "title": a.title or "",
                        "description": a.description or "",
                        "priority": a.priority or "",
                        "type": a.type or "",
                        "assignee_suggestion": a.assignee_suggestion or ""
                    } for a in actions
                ],
                "deck": {
                    "deck_title": deck.deck_title if deck else "",
                    "slides": deck.slides if deck and deck.slides else []
                },
                "talking_points": talking_points.talking_points if talking_points and talking_points.talking_points else []
            }
        

        return jsonify(ui_json)

    finally:
        db.close()

