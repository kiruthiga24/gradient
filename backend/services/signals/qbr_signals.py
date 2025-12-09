from datetime import datetime
from sqlalchemy import func
from models.base_model import Signals, Contracts, Orders, UsageMetrics, QualityIncidents
from ..utils.base import normalize
from ..utils.base import to_json_safe


def detect_qbr_ready(db, agent_run_id):
    rows = db.query(Contracts).all()
    results = []

    for c in rows:
        if not c.end_date:
            continue

        days = (c.end_date - datetime.utcnow().date()).days

        if 0 <= days <= 45:
            rev = db.query(func.sum(Orders.total_amount))\
                    .filter(Orders.account_id == c.account_id).scalar() or 0

            usage = db.query(func.sum(UsageMetrics.usage_volume))\
                    .filter(UsageMetrics.account_id == c.account_id).scalar() or 0

            defects = db.query(QualityIncidents)\
                        .filter(QualityIncidents.account_id == c.account_id).count()
            
            extras = to_json_safe({
                "rev": rev,
                "usage": usage,
                "defects": defects,
                "days": days
            })

            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=c.account_id,
                signal_type="qbr_due",
                signal_strength=1.0,
                extras=extras
            ))

    db.add_all(results)
    db.commit()
    return results
