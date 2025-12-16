from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals, QualityIncidents
from ..utils.base import normalize

BASELINE_DAYS = 90
RECENT_DAYS = 30
SPIKE_THRESHOLD = 1.5

def detect_quality_spike(db, agent_run_id):
    cutoff = datetime.utcnow().date() - timedelta(days=BASELINE_DAYS)

    rows = db.query(
        QualityIncidents.account_id,
        QualityIncidents.incident_date
    ).filter(
        QualityIncidents.incident_date >= cutoff
    ).all()

    grouped = {}
    for r in rows:
        grouped.setdefault(r.account_id, []).append(r.incident_date)

    results = []
    split = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)

    for acct, dates in grouped.items():
        baseline = len([d for d in dates if d < split])
        recent = len([d for d in dates if d >= split])

        base_rate = baseline / (BASELINE_DAYS - RECENT_DAYS) if baseline else 1
        recent_rate = recent / RECENT_DAYS

        ratio = recent_rate / base_rate if base_rate else 0

        if ratio >= SPIKE_THRESHOLD:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="quality_spike",
                signal_strength=normalize(ratio),
                extras={"baseline": baseline, "recent": recent, "ratio": ratio}
            ))

    db.add_all(results)
    db.commit()
    return results
