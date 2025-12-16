from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals, UsageMetrics
from ..utils.base import normalize

RECENT_DAYS = 30
BASELINE_DAYS = 60
DROP_THRESHOLD = 0.25

def detect_usage_decline(db, agent_run_id):
    cutoff = datetime.utcnow() - timedelta(days=BASELINE_DAYS)

    rows = db.query(
        UsageMetrics.account_id,
        UsageMetrics.usage_date,
        func.sum(UsageMetrics.usage_volume).label("vol")
    ).filter(
        UsageMetrics.usage_date >= cutoff
    ).group_by(
        UsageMetrics.account_id, UsageMetrics.usage_date
    ).all()

    grouped = {}
    for r in rows:
        grouped.setdefault(r.account_id, []).append((r.usage_date, float(r.vol)))

    results = []
    split_date = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)

    for acct, values in grouped.items():
        prev = [v for d, v in values if d < split_date]
        recent = [v for d, v in values if d >= split_date]

        prev_avg = sum(prev)/len(prev) if prev else 0
        recent_avg = sum(recent)/len(recent) if recent else 0

        drop = (prev_avg - recent_avg) / prev_avg if prev_avg else 0
        if drop >= DROP_THRESHOLD:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="usage_decline",
                signal_strength=normalize(drop),
                extras={"baseline": prev_avg, "recent": recent_avg, "drop": drop}
            ))

    db.add_all(results)
    db.commit()
    return results
