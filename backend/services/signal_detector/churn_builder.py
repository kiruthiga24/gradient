from models.base_model import ChurnRiskAssessments

CHURN_TYPES = {
    "order_volume_drop", "usage_decline", "quality_spike",
    "oee_drop", "shipment_delay_risk", "support_ticket_spike"
}

def build_churn_assessments(db, signals):
    rows = []
    for s in signals:
        if s.signal_type in CHURN_TYPES:
            score = float(s.signal_strength)
            level = "High" if score >= 0.7 else "Medium" if score >= 0.4 else "Low"

            rows.append(ChurnRiskAssessments(
                signal_id=s.signal_id,
                account_id=s.account_id,
                risk_score=score,
                risk_level=level
            ))

    db.add_all(rows)
    db.commit()
