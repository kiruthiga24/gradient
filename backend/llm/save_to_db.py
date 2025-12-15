# scripts/insert_expansion_rca.py

import uuid
from models.base_model import ExpansionRcaAnalysis, ExpansionBrief, ExpansionDeck, ExpansionRecommendation, ExpansionRevenueEstimate, \
      QbrAction, QbrBrief, QbrDeck, QbrOpportunity, QbrRcaAnalysis, QbrTalkingPoints, RcaAnalysis, ChurnBriefs, Recommendations, EmailDrafts, \
      SupplyRca, SupplyBrief, SupplyAction, SupplyEmail


from models.base_model import (
    QualityRcaAnalysis,
    QualityBrief,
    QualityAction,
    QualityEmail,
)

def insert_expansion_rca(db, rca, agent_run_id, account_id):
    try:
        row = ExpansionRcaAnalysis(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,  # replace with real agent_run_id if available
            account_id=account_id,
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

def insert_churn_rca(db, rca, agent_run_id, account_id):
    try:
        row = RcaAnalysis(
            rca_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            severity=rca.get("severity", ""),
            business_impact=rca.get("business_impact", ""),
            confidence_score=rca.get("confidence_score", 0.0),
            root_causes=rca.get("root_causes", [])  # JSON column
        )

        db.add(row)
        db.commit()
        print("✅ RCA Insert successful")

    except Exception as e:
        db.rollback()
        print("❌ RCA Insert failed:", str(e))


def insert_churn_brief(db, brief, agent_run_id, account_id):
    try:
        row = ChurnBriefs(
            brief_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            title=brief.get("title", ""),
            exec_summary=brief.get("exec_summary", ""),
            key_drivers=brief.get("key_drivers", []),          # JSON list
            recommended_focus=brief.get("recommended_focus", ""),
            risk_level=brief.get("risk_level", "")
        )

        db.add(row)
        db.commit()
        print("✅ Brief Insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Brief Insert failed:", str(e))


def insert_churn_action(db, action, agent_run_id, account_id):
    try:
        row = Recommendations(
            recommendation_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            action_details=action.get("action", ""),
            owner=action.get("owner", ""),
            due_date=action.get("due_date", None),
            priority=action.get("priority", "")
        )

        db.add(row)
        db.commit()
        print("✅ Action Insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Action Insert failed:", str(e))


def insert_churn_email(db, email, agent_run_id, account_id):
    try:
        row = EmailDrafts(
            email_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            subject=email.get("subject", ""),
            body_text=email.get("body_text", "")
        )

        db.add(row)
        db.commit()
        print("✅ Email Insert successful")

    except Exception as e:
        db.rollback()
        print("❌ Email Insert failed:", str(e))


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

def insert_expansion_revenue(db, revenue, agent_run_id, account_id):
    try:
        row = ExpansionRevenueEstimate(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_expansion_recommendations(db, actions, agent_run_id, account_id):
    try:
        for idx, act in enumerate(actions.get("actions", []), start=1):

            row = ExpansionRecommendation(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                account_id=account_id,
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

def insert_expansion_deck(db, deck, agent_run_id, account_id):
    try:
        slides = deck.get("slides", [])

        row = ExpansionDeck(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_qbr_rca(db, rca, agent_run_id, account_id):
    try:
        row = QbrRcaAnalysis(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_qbr_brief(db, brief, agent_run_id, account_id):
    try:
        row = QbrBrief(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_qbr_opportunities(db, opportunities, agent_run_id, account_id):
    try:
        for opp in opportunities.get("opportunities", []):
            row = QbrOpportunity(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                account_id=account_id,
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

def insert_qbr_actions(db, actions, agent_run_id, account_id):
    try:
        for act in actions.get("actions", []):
            row = QbrAction(
                id=uuid.uuid4(),
                agent_run_id=agent_run_id,
                account_id=account_id,
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

def insert_qbr_deck(db, deck, agent_run_id, account_id):
    try:
        slides = deck.get("slides", [])
        row = QbrDeck(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_qbr_talking_points(db, talking_points, agent_run_id, account_id):
    try:
        row = QbrTalkingPoints(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
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

def insert_supply_rca(db, rca, agent_run_id, account_id):
    try:
        row = SupplyRca(
            rca_id = uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            severity=rca.get("severity", ""),
            confidence_score=rca.get("confidence_score", 0.0),
            business_impact=rca.get("business_impact", ""),
            root_causes=rca.get("root_causes", [])
        )
        db.add(row)
        db.commit()
        print("✅ RCA Insert successful")
    except Exception as e:
        db.rollback()
        print("❌ RCA Insert failed:", str(e))

def insert_supply_brief(db, brief, agent_run_id, account_id):
    try:
        row = SupplyBrief(
            brief_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            
            account_id=account_id,
            situation=brief.get("situation", ""),
            priority=brief.get("priority", ""),
            urgency_score=brief.get("urgency_score", 0),
            key_metrics=brief.get("key_metrics", {})
        )
        db.add(row)
        db.commit()
        print("✅ Brief Insert successful")
    except Exception as e:
        db.rollback()
        print("❌ Brief Insert failed:", str(e))

def insert_supply_actions(db, actions, agent_run_id, account_id):
    try:
        row = SupplyAction(
            action_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            immediate_action=actions.get("immediate_actions", []),
            follow_up_action=actions.get("followup_actions", []),
            owner=actions.get("owners", []),
            timeline=actions.get("timeline", ""),
            success_criteria=actions.get("success_criteria", [])
        )
        db.add(row)
        db.commit()
        print("✅ Actions Insert successful")   
    except Exception as e:
        db.rollback()
        print("❌ Actions Insert failed:", str(e))

def insert_supply_email(db, email, agent_run_id, account_id):
    try:
        row = SupplyEmail(
            email_id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            account_id=account_id,
            subject=email.get("subject", ""),
            body_text=email.get("body", ""),
            priority=email.get("priority", ""),
            recipients=email.get("recipients", []),
            cc=email.get("cc", [])
        )
        db.add(row)
        db.commit()
        print("✅ Email Insert successful")
    except Exception as e:
        db.rollback()
        print("❌ Email Insert failed:", str(e))

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
    insert_expansion_rca(db, payload["rca"], agent_run_id, payload["account_id"])
    insert_expansion_brief(db, payload["brief"], agent_run_id, payload["account_id"])
    insert_expansion_revenue(db, payload["revenue"], agent_run_id, payload["account_id"])
    insert_expansion_recommendations(db, payload["actions"], agent_run_id, payload["account_id"])
    insert_expansion_deck(db, payload["deck"], agent_run_id, payload["account_id"])

def save_qbr_output(db, payload, agent_run_id):
    insert_qbr_rca(db, payload["rca"], agent_run_id, payload["account_id"])
    insert_qbr_brief(db, payload["brief"], agent_run_id, payload["account_id"])
    insert_qbr_opportunities(db, payload["opportunities"], agent_run_id, payload["account_id"])
    insert_qbr_actions(db, payload["actions"], agent_run_id, payload["account_id"])
    insert_qbr_deck(db, payload["deck"], agent_run_id, payload["account_id"])
    insert_qbr_talking_points(db, payload["talking_points"], agent_run_id, payload["account_id"])

# Orchestrated save wrapper

def save_quality_output(db, payload, agent_run_id):
    insert_quality_rca(db, payload["rca"], agent_run_id, payload["account_id"])
    insert_quality_brief(db, payload["brief"], agent_run_id, payload["account_id"])
    insert_quality_actions(db, payload["actions"], agent_run_id, payload["account_id"])
    insert_quality_email(db, payload["email"], agent_run_id, payload["account_id"])

def save_churn_output(db, payload, agent_run_id, account_id):
    insert_churn_rca(db, payload["rca"], agent_run_id, account_id)
    insert_churn_brief(db, payload["brief"], agent_run_id,account_id )
    for action in payload["actions"]["actions"]:
        insert_churn_action(db, action, agent_run_id, account_id)
    insert_churn_email(db, payload["email"], agent_run_id, account_id)

def save_supply_output(db, payload, agent_run_id, account_id):
    insert_supply_rca(db, payload["rca"], agent_run_id,account_id )
    insert_supply_brief(db, payload["brief"], agent_run_id, account_id)
    insert_supply_actions(db, payload["actions"], agent_run_id, account_id)
    insert_supply_email(db, payload["email"], agent_run_id, account_id)
    

