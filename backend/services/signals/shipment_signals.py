from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals, Shipments, Orders
from ..utils.base import normalize


RECENT_DAYS = 30
DELAY_THRESHOLD = 0.2

def detect_shipment_delays(db, agent_run_id):
    cutoff = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)

    rows = db.query(
        Orders.account_id,
        Shipments.delivery_status
    ).join(
        Orders, Shipments.order_id == Orders.order_id
    ).filter(
        Shipments.shipment_date >= cutoff
    ).all()

    grouped = {}
    for r in rows:
        grouped.setdefault(r.account_id, []).append(r.delivery_status)

    results = []

    for acct, statuses in grouped.items():
        total = len(statuses)
        delayed = len([s for s in statuses if "delay" in (s or "").lower()])
        ratio = delayed / total if total else 0

        if ratio >= DELAY_THRESHOLD:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="shipment_delay_risk",
                signal_strength=normalize(ratio),
                extras={"total": total, "delayed": delayed}
            ))

    db.add_all(results)
    db.commit()
    return results
