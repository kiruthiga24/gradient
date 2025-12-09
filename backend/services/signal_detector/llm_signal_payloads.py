import uuid
from datetime import datetime
from models.base_model import Signals, Accounts, LLMSignalPayloads

# ---------------------
# Signal group mapping
# ---------------------
USE_CASE_MAP = {
    "churn_risk": ["order_volume_drop", "usage_decline", "quality_spike", "oee_drop", "support_ticket_spike", "shipment_delay_risk"],
    "expansion_opportunity": ["expansion_opportunity"],
    "quality_incident": ["quality_spike"],
    "supply_risk": ["shipment_delay_risk"],
    "qbr_auto_generation": ["qbr_due"]
}

SIGNAL_WEIGHTS = {
    "order_volume_drop": 0.30,
    "usage_decline": 0.20,
    "quality_spike": 0.20,
    "oee_drop": 0.10,
    "support_ticket_spike": 0.10,
    "shipment_delay_risk": 0.10,
    "expansion_opportunity": 0.60,
    "cross_sell_whitespace": 0.40,
    "qbr_due": 1.00
}

def uid():
    return uuid.uuid4()

# ---------------------
# Build payloads
# ---------------------
def build_llm_payloads(db, signals):
    account_map = {}
    for s in signals:
        account_map.setdefault(s.account_id, []).append(s)

    payload_rows = []
    for account_id, acc_signals in account_map.items():
        # Use agent_run_id from the first signal for this account
        agent_run_id = acc_signals[0].agent_run_id

        # Fetch account_name
        account_name = db.query(Accounts.account_name).filter(Accounts.account_id == account_id).scalar()

        for use_case, signal_types in USE_CASE_MAP.items():
            uc_signals = [s for s in acc_signals if s.signal_type in signal_types]
            if not uc_signals:
                continue

            total_score = 0
            total_weight = 0
            evidence = []

            for s in uc_signals:
                w = SIGNAL_WEIGHTS.get(s.signal_type, 0.1)
                total_score += float(s.signal_strength) * w
                total_weight += w
                extras_serializable = {k: str(v) if isinstance(v, uuid.UUID) else v for k, v in (s.extras or {}).items()}
                evidence.append({
                    "signal_type": s.signal_type,
                    "strength": float(s.signal_strength),
                    "raw_data": extras_serializable
                })

            final_score = round(total_score / max(total_weight, 0.01), 2)

            # Classify risk level
            if use_case == "churn_risk":
                if final_score >= 0.7:
                    risk_level = "HIGH"
                elif final_score >= 0.4:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
            else:
                risk_level = "N/A"

            payload_json = {
                "use_case": use_case,
                "account": {
                    "account_id": str(account_id),
                    "account_name": account_name
                },
                "final_score": final_score,
                "risk_level": risk_level,
                "signals": evidence,
                "generated_at": datetime.utcnow().isoformat()
            }

            payload_rows.append(LLMSignalPayloads(
                payload_id=uid(),
                agent_run_id=agent_run_id,
                account_id=account_id,
                use_case_name=use_case,
                final_score=final_score,
                payload_json=payload_json
            ))

    if payload_rows:
        db.add_all(payload_rows)
        db.commit()

    return payload_rows

# ---------------------
# Main
# ---------------------
# def main():
#     db = db_session()
#     recent_signals = db.query(Signals).filter(Signals.detected_at >= datetime.utcnow().date()).all()
#     payloads = build_llm_payloads(db, recent_signals)
#     print(f"Generated {len(payloads)} LLM payloads")
#     db.close()
