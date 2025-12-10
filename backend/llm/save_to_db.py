# scripts/insert_expansion_rca.py

import uuid
from models.base_model import ExpansionRcaAnalysis, ExpansionBrief, ExpansionDeck, ExpansionRecommendation, ExpansionRevenueEstimate


def insert_expansion_rca(db, rca, agent_run_id):
    try:
        row = ExpansionRcaAnalysis(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,  # replace with real agent_run_id if available
            usage_anomalies=rca.get("usage_anomalies"),
            competitor_dependency=rca.get("competitor_dependency"),
            bom_gaps=rca.get("bom_gaps"),
            revenue_leakage_estimate=rca.get("revenue_leakage_estimate")
        )

        db.add(row)
        db.commit()
        print("✅ Insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Insert failed:", str(e))

    finally:
        db.close()

def insert_expansion_brief(db, brief, agent_run_id):
    try:
        row = ExpansionBrief(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,

            brief_summary=brief.get("executive_summary"),

            whitespace_opportunities=brief.get("detected_patterns", []),
            cross_sell_targets=[],   # not available in this LLM output

            created_at=None
        )

        db.add(row)
        db.commit()
        print("✅ Brief insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Brief insert failed:", str(e))

    finally:
        db.close()

def insert_expansion_revenue(db, revenue, agent_run_id):
    try:
        row = ExpansionRevenueEstimate(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,

            estimated_monthly_revenue=revenue.get("total_estimated_monthly_revenue", 0),
            estimated_annual_revenue=revenue.get("total_estimated_monthly_revenue", 0) * 12,

            currency="USD",

            assumptions=revenue.get("assumptions", [])
        )

        db.add(row)
        db.commit()
        print("✅ Revenue insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Revenue insert failed:", str(e))

    finally:
        db.close()

def insert_expansion_recommendations(db, actions, agent_run_id):
    try:
        for idx, act in enumerate(actions.get("actions", []), start=1):

            row = ExpansionRecommendation(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,

                priority=1 if act["priority"] == "High" else 2,

                recommendation_type=act.get("action_type"),

                target_sku=None,  # not provided

                rationale=f"{act.get('title')} - {act.get('description')}",

                expected_lift=None
            )

            db.add(row)

        db.commit()
        print("✅ Recommendations insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Recommendations insert failed:", str(e))

    finally:
        db.close()

def insert_expansion_deck(db, deck, agent_run_id):
    try:
        slides = deck.get("slides", [])

        row = ExpansionDeck(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,

            deck_title="Expansion Opportunity Analysis",
            slide_count=len(slides),

            deck_outline=slides
        )

        db.add(row)
        db.commit()
        print("✅ Deck insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Deck insert failed:", str(e))

    finally:
        db.close()


def save_expansion_output(db, payload, agent_run_id):
    insert_expansion_rca(db, payload["rca"], agent_run_id)
    insert_expansion_brief(db, payload["brief"], agent_run_id)
    insert_expansion_revenue(db, payload["revenue"], agent_run_id)
    insert_expansion_recommendations(db, payload["actions"], agent_run_id)
    insert_expansion_deck(db, payload["deck"], agent_run_id)
