from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals
from ..utils.base import normalize
from models.base_model import UsageMetrics

BASELINE_DAYS = 90
RECENT_DAYS = 30
GROWTH_THRESHOLD = 0.15

def detect_expansion(db, agent_run_id):
    cutoff = datetime.utcnow().date() - timedelta(days=BASELINE_DAYS)

    rows = db.query(
        UsageMetrics.account_id,
        UsageMetrics.usage_date,
        func.sum(UsageMetrics.usage_volume)
    ).filter(
        UsageMetrics.usage_date >= cutoff
    ).group_by(
        UsageMetrics.account_id, UsageMetrics.usage_date
    ).all()

    grouped = {}

    for r in rows:
        acct, dt, vol = r
        grouped.setdefault(acct, []).append((dt, float(vol)))

    results = []
    split = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)

    for acct, vals in grouped.items():
        base = [v for d, v in vals if d < split]
        rec = [v for d, v in vals if d >= split]

        base_avg = sum(base)/len(base) if base else 0
        rec_avg = sum(rec)/len(rec) if rec else 0

        growth = (rec_avg - base_avg)/base_avg if base_avg else 0

        if growth >= GROWTH_THRESHOLD:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="expansion_opportunity",
                signal_strength=normalize(growth),
                extras={"baseline": base_avg, "recent": rec_avg}
            ))

    db.add_all(results)
    db.commit()
    return results
