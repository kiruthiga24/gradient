# scripts/insert_expansion_rca.py

import uuid
from models.base_model import ExpansionRcaAnalysis, ExpansionBrief, ExpansionDeck, ExpansionRecommendation, ExpansionRevenueEstimate, QbrAction, QbrBrief, QbrDeck, QbrOpportunity, QbrRcaAnalysis, QbrTalkingPoints

from models.base_model import (
    QualityRcaAnalysis,
    QualityBrief,
    QualityAction,
    QualityEmail,
)

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

def insert_qbr_rca(db, rca, agent_run_id):
    try:
        row = QbrRcaAnalysis(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            trends=rca.get("trends"),
            root_causes=rca.get("root_causes"),
            signals=rca.get("signals"),
            kpi_summary=rca.get("kpi_summary")
        )
        db.add(row)
        db.commit()
        print("✅ QBR RCA insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR RCA insert failed:", str(e))
    finally:
        db.close()

def insert_qbr_brief(db, brief, agent_run_id):
    try:
        row = QbrBrief(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            executive_summary=brief.get("executive_summary"),
            key_wins=brief.get("key_wins", []),
            key_risks=brief.get("key_risks", []),
            opportunities_summary=brief.get("opportunities_summary", [])
        )
        db.add(row)
        db.commit()
        print("✅ QBR Brief insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR Brief insert failed:", str(e))
    finally:
        db.close()

def insert_qbr_opportunities(db, opportunities, agent_run_id):
    try:
        for opp in opportunities.get("opportunities", []):
            row = QbrOpportunity(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                type=opp.get("type"),
                sku=opp.get("sku"),
                rationale=opp.get("rationale"),
                estimated_value=opp.get("estimated_value")
            )
            db.add(row)
        db.commit()
        print("✅ QBR Opportunities insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR Opportunities insert failed:", str(e))
    finally:
        db.close()

def insert_qbr_actions(db, actions, agent_run_id):
    try:
        for act in actions.get("actions", []):
            row = QbrAction(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                title=act.get("title"),
                description=act.get("description"),
                priority=act.get("priority"),
                type=act.get("type"),
                assignee_suggestion=act.get("assignee_suggestion")
            )
            db.add(row)
        db.commit()
        print("✅ QBR Actions insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR Actions insert failed:", str(e))
    finally:
        db.close()

def insert_qbr_deck(db, deck, agent_run_id):
    try:
        slides = deck.get("slides", [])
        row = QbrDeck(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            deck_title=deck.get("deck_title", "QBR Deck"),
            slides=slides
        )
        db.add(row)
        db.commit()
        print("✅ QBR Deck insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR Deck insert failed:", str(e))
    finally:
        db.close()

def insert_qbr_talking_points(db, talking_points, agent_run_id):
    try:
        row = QbrTalkingPoints(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            talking_points=talking_points.get("talking_points", [])
        )
        db.add(row)
        db.commit()
        print("✅ QBR Talking Points insert successful")
    except Exception as e:
        db.rollback()
        print("❌ QBR Talking Points insert failed:", str(e))
    finally:
        db.close()


def insert_quality_rca(db, rca, agent_run_id, account_id):
    try:
        row = QualityRcaAnalysis(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            correlated_factors=rca.get("correlated_factors", {}),
            trends=rca.get("trends", {}),
            defect_patterns=rca.get("defect_patterns", {}),
            total_incidents=rca.get("total_incidents", 0),
            notes=rca.get("notes"),
        )

        db.add(row)
        db.commit()
        print("✅ Quality RCA insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Quality RCA insert failed:", str(e))


def insert_quality_brief(db, brief, agent_run_id, account_id):
    try:
        row = QualityBrief(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            executive_summary=brief.get("executive_summary"),
            key_findings=brief.get("key_findings", []),
            risk_level=brief.get("risk_level"),
            impact_estimate=brief.get("impact_estimate"),
        )

        db.add(row)
        db.commit()
        print("✅ Quality Brief insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Quality Brief insert failed:", str(e))


def insert_quality_actions(db, actions, agent_run_id, account_id):
    try:
        for act in actions.get("actions", []):
            row = QualityAction(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                account_id=account_id,
                title=act.get("title"),
                description=act.get("description"),
                priority=act.get("priority"),
                action_type=act.get("action_type"),
                assignee_suggestion=act.get("assignee_suggestion"),
                expected_impact=act.get("expected_impact", {}),
            )
            db.add(row)

        db.commit()
        print("✅ Quality Actions insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Quality Actions insert failed:", str(e))


def insert_quality_email(db, email, agent_run_id, account_id):
    try:
        row = QualityEmail(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            subject=email.get("subject"),
            body=email.get("body"),
            to_address=email.get("to_address"),
        )

        db.add(row)
        db.commit()
        print("✅ Quality Email insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Quality Email insert failed:", str(e))

def save_expansion_output(db, payload, agent_run_id):
    insert_expansion_rca(db, payload["rca"], agent_run_id)
    insert_expansion_brief(db, payload["brief"], agent_run_id)
    insert_expansion_revenue(db, payload["revenue"], agent_run_id)
    insert_expansion_recommendations(db, payload["actions"], agent_run_id)
    insert_expansion_deck(db, payload["deck"], agent_run_id)

def save_qbr_output(db, payload, agent_run_id):
    insert_qbr_rca(db, payload["rca"], agent_run_id)
    insert_qbr_brief(db, payload["brief"], agent_run_id)
    insert_qbr_opportunities(db, payload["opportunities"], agent_run_id)
    insert_qbr_actions(db, payload["actions"], agent_run_id)
    insert_qbr_deck(db, payload["deck"], agent_run_id)
    insert_qbr_talking_points(db, payload["talking_points"], agent_run_id)

# Orchestrated save wrapper

def save_quality_output(db, payload, agent_run_id):
    insert_quality_rca(db, payload["rca"], agent_run_id, payload["account_id"])
    insert_quality_brief(db, payload["brief"], agent_run_id, payload["account_id"])
    insert_quality_actions(db, payload["actions"], agent_run_id, payload["account_id"])
    insert_quality_email(db, payload["email"], agent_run_id, payload["account_id"])

