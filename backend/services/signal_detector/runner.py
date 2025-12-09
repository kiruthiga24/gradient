import uuid
from datetime import datetime
from models.base_model import AgentRuns, Signals
from database import SessionLocal
from utils.logger import logger


from services.signals.order_signals import detect_order_volume_drop
from services.signals.usage_signals import detect_usage_decline
from services.signals.quality_signals import detect_quality_spike
from services.signals.oee_signals import detect_oee_drop
from services.signals.shipment_signals import detect_shipment_delays
from services.signals.support_signals import detect_support_spike
from services.signals.expansion_signals import detect_expansion
from services.signals.whitespace_signals import detect_whitespace
from services.signals.qbr_signals import detect_qbr_ready
from services.signal_detector.churn_builder import build_churn_assessments
from services.signal_detector.llm_signal_payloads import build_llm_payloads

def run_all_detectors(db):
    agent_run_id = str(uuid.uuid4())
    logger.info("inside runner")

    run = AgentRuns(
        agent_run_id=agent_run_id,
        run_timestamp=datetime.utcnow(),
        run_type="manual",
        status="running"
    )

    db.add(run)
    db.commit()

    
    # Run detectors
    total = 0
    detectors = [
        detect_order_volume_drop,
        detect_usage_decline,
        detect_quality_spike,
        detect_oee_drop,
        detect_shipment_delays,
        detect_support_spike,
        detect_expansion,
        # detect_whitespace, #no value
        detect_qbr_ready
    ]

    for d in detectors:
        res = d(db, agent_run_id)
        total += len(res)


    # Mark run completed
    run.status = "completed"
    db.commit()

    all_signals = db.query(Signals).all()
    build_churn_assessments(db, all_signals)
    build_llm_payloads(db, all_signals)

    return {
        "agent_run_id": agent_run_id,
        "total_signals": total
    }
