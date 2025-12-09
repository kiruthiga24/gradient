from sqlalchemy import func
from datetime import datetime, timedelta
from models.base_model import Signals
from ..utils.base import normalize
from models.base_model import OeeMetrics
from models.base_model import Plants
from ..utils.base import to_json_safe


BASELINE_DAYS = 90
RECENT_DAYS = 30
DROP_THRESHOLD = 0.05

def detect_oee_drop(db, agent_run_id):
    cutoff = datetime.utcnow().date() - timedelta(days=BASELINE_DAYS)

    rows = db.query(
        OeeMetrics.plant_id,
        OeeMetrics.metric_date,
        OeeMetrics.oee_score
    ).filter(
        OeeMetrics.metric_date >= cutoff
    ).all()
    print("*******")
    print(len(rows))
    plant_map = {
        p.plant_id: p.account_id
        for p in db.query(Plants).all()
    }
    print(len(plant_map))
    print(plant_map)

    grouped = {}

    for r in rows:
        grouped.setdefault(r.plant_id, []).append((r.metric_date, float(r.oee_score)))
    print("Grouped plant count:", len(grouped))


    results = []
    split = datetime.utcnow().date() - timedelta(days=RECENT_DAYS)

    for plant, values in grouped.items():
        prev = [v for d, v in values if d < split]
        recent = [v for d, v in values if d >= split]

        prev_avg = sum(prev)/len(prev) if prev else 0
        recent_avg = sum(recent)/len(recent) if recent else 0

        drop = (prev_avg - recent_avg) / prev_avg if prev_avg else 0

        acct = plant_map.get(plant)
        extras = to_json_safe({"plant": str(plant), "baseline": prev_avg, "recent": recent_avg})
        print("drop$$$$$$$$", drop)

        if drop >= DROP_THRESHOLD and acct:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="oee_drop",
                signal_strength=normalize(drop),
                extras=extras
            ))

    db.add_all(results)
    db.commit()
    return results
