from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals
from models.base_model import Orders  # your existing model
from ..utils.base import normalize

RECENT_DAYS = 30
BASELINE_DAYS = 90
ORDER_DROP_THRESHOLD = 0.25

def detect_order_volume_drop(db, agent_run_id):
    print("inside order volume drop")
    cutoff_recent = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)
    cutoff_base = datetime.utcnow().date() - timedelta(days=RECENT_DAYS + BASELINE_DAYS)

    rows = db.query(
        Orders.account_id,
        Orders.order_date,
        func.sum(Orders.total_amount).label("amt")
    ).filter(
        Orders.order_date >= cutoff_base
    ).group_by(
        Orders.account_id, Orders.order_date
    ).all()

    result = []
    grouped = {}

    for r in rows:
        grouped.setdefault(r.account_id, []).append((r.order_date, float(r.amt)))

    for acct, values in grouped.items():
        base = [v for d, v in values if d < cutoff_recent]
        recent = [v for d, v in values if d >= cutoff_recent]

        base_avg = sum(base)/len(base) if base else 0
        recent_avg = sum(recent)/len(recent) if recent else 0

        drop = (base_avg - recent_avg) / base_avg if base_avg else 0
        if drop >= ORDER_DROP_THRESHOLD:
            result.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="order_volume_drop",
                signal_strength=normalize(drop),
                extras={"baseline": base_avg, "recent": recent_avg, "drop": drop}
            ))

    db.add_all(result)
    db.commit()
    return result
