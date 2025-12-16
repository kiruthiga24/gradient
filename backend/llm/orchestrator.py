import json, uuid, re
import json
from decimal import Decimal
from datetime import datetime, timedelta
from models.base_model import QualityIncidents

from .rag_seed.rag_store import query_docs
from .llm_factory import get_llm
from .save_to_db import save_expansion_output, save_qbr_output, save_churn_output, save_supply_output, save_quality_output
import re



from .churn_chains.rca_chain import build_rca_chain
from .churn_chains.brief_chain import build_brief_chain
from .churn_chains.action_chain import build_action_chain
from .churn_chains.email_chain import build_email_chain

from .expansion_chains.action_chain import build_expansion_action_chain
from .expansion_chains.brief_chain import build_expansion_brief_chain
from .expansion_chains.deck_chain import build_expansion_deck_chain
from .expansion_chains.rca_chain import build_expansion_rca_chain
from .expansion_chains.revenue_chain import build_expansion_revenue_chain

from .qbr_chains.action_chain import build_qbr_action_chain
from .qbr_chains.brief_chain import build_qbr_brief_chain
from .qbr_chains.deck_chain import build_qbr_deck_chain
from .qbr_chains.opportunities_chain import build_qbr_opportunity_chain
from .qbr_chains.rca_chain import build_qbr_rca_chain
from .qbr_chains.talking_chain import build_qbr_talk_chain 

from .quality_chain.rca_chain import build_quality_rca_chain
from .quality_chain.brief_chain import build_quality_brief_chain
from .quality_chain.action_chain import build_quality_action_chain
from .quality_chain.email_chain import build_quality_email_chain

# and reuse json_safe, parse_json_safe already in file

from .supply_chains.action_chain import build_supply_action_chain
from .supply_chains.brief_chain import build_supply_brief_chain
from .supply_chains.email_chain import build_supply_email_chain
from .supply_chains.rca_chain import build_supply_rca_chain



def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def json_safe(obj) -> str:
    """Ensure obj is a JSON string."""
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, ensure_ascii=False)

def parse_json_safe(raw):
    """
    Best-effort parse for LLM outputs:
    - If already dict, return it
    - If valid JSON string, json.loads
    - Else extract first {...} JSON block and try to parse
    - Else return {'_raw': raw}
    """
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, (list, int, float, bool)):
        return {"value": raw}
    # try direct parse
    try:
        return json.loads(raw)
    except Exception:
        pass
    # attempt extract JSON object
    try:
        m = re.search(r'(\{.*\})', raw, re.DOTALL)
        if m:
            block = m.group(1)
            return json.loads(block)
    except Exception:
        pass
    # fallback - keep raw string under _raw
    return {"_raw": str(raw)}


class LLMOrchestrator:
    def __init__(self):
        self.llm = None

        self.rca_chain = None
        self.brief_chain = None
        self.action_chain = None
        self.email_chain = None

         # ---------- Use Case 2: Expansion ----------
        self.expansion_rca_chain = None
        self.expansion_brief_chain = None
        self.expansion_revenue_chain = None
        self.expansion_action_chain = None
        self.expansion_deck_chain = None

         # ---------- Use Case 3: QBR ----------
        self.qbr_rca_chain = None
        self.qbr_brief_chain = None
        self.qbr_opportunity_chain = None
        self.qbr_action_chain = None
        self.qbr_deck_chain = None
        self.qbr_talk_chain = None

        # ---------- Use Case 4: Quality -----------
        self.quality_rca_chain = None
        self.quality_brief_chain = None
        self.quality_action_chain = None
        self.quality_email_chain = None
        # ---------- Use Case 4: Supply Risk ----------
        self.supply_risk_rca_chain = None
        self.supply_risk_brief_chain = None
        self.supply_risk_action_chain = None
        self.supply_risk_email_chain = None

        self._init_llm()
    
    # ----------------------------
    # Init LLM only once
    # ----------------------------
    def _init_llm(self):
        if self.llm is None:
            self.llm = get_llm()
    
    def _initialize_chains(self):
        """Lazy initialization of chains"""    
        if self.rca_chain is None:
            self.rca_chain = build_rca_chain(self.llm)
        if self.brief_chain is None:
            self.brief_chain = build_brief_chain(self.llm)
        if self.action_chain is None:
            self.action_chain = build_action_chain(self.llm)
        if self.email_chain is None:
            self.email_chain = build_email_chain(self.llm)

    def _init_supply_risk_chains(self):
        if self.supply_risk_rca_chain is None:
            self.supply_risk_rca_chain = build_supply_rca_chain(self.llm)

        if self.supply_risk_brief_chain is None:
            self.supply_risk_brief_chain = build_supply_brief_chain(self.llm)

        if self.supply_risk_action_chain is None:
            self.supply_risk_action_chain = build_supply_action_chain(self.llm)

        if self.supply_risk_email_chain is None:
            self.supply_risk_email_chain = build_supply_email_chain(self.llm)
    
    def _init_expansion_chains(self):
        if self.expansion_rca_chain is None:
            self.expansion_rca_chain = build_expansion_rca_chain(self.llm)

        if self.expansion_brief_chain is None:
            self.expansion_brief_chain = build_expansion_brief_chain(self.llm)

        if self.expansion_revenue_chain is None:
            self.expansion_revenue_chain = build_expansion_revenue_chain(self.llm)

        if self.expansion_action_chain is None:
            self.expansion_action_chain = build_expansion_action_chain(self.llm)

        if self.expansion_deck_chain is None:
            self.expansion_deck_chain = build_expansion_deck_chain(self.llm)

    def _init_qbr_chains(self):
        if self.qbr_rca_chain is None:
            self.qbr_rca_chain = build_qbr_rca_chain(self.llm)

        if self.qbr_brief_chain is None:
            self.qbr_brief_chain = build_qbr_brief_chain(self.llm)

        if self.qbr_opportunity_chain is None:
            self.qbr_opportunity_chain = build_qbr_opportunity_chain(self.llm)

        if self.qbr_action_chain is None:
            self.qbr_action_chain = build_qbr_action_chain(self.llm)

        if self.qbr_deck_chain is None:
            self.qbr_deck_chain = build_qbr_deck_chain(self.llm)

        if self.qbr_talk_chain is None:
            self.qbr_talk_chain = build_qbr_talk_chain(self.llm)
    
    def _init_quality_chains(self):
        if self.quality_rca_chain is None:
            self.quality_rca_chain = build_quality_rca_chain(self.llm)

        if self.quality_brief_chain is None:
            self.quality_brief_chain = build_quality_brief_chain(self.llm)

        if self.quality_action_chain is None:
            self.quality_action_chain = build_quality_action_chain(self.llm)
            
        if self.quality_email_chain is None:
            self.quality_email_chain = build_quality_email_chain(self.llm)

    
    # ----------------------------
    # Entry point
    # ----------------------------
    def run_pipeline(self, db, use_case: str, payload: dict, agent_run_id: uuid):
        """
        use_case:
          - "churn"
          - "expansion"
        """
        if use_case == "churn_risk":
            churn_payload = self._run_churn_pipeline(payload)
            print(json.dumps(churn_payload, indent=4, sort_keys=True))
            save_churn_output(db, churn_payload, agent_run_id, payload["account"]["account_id"])
            return churn_payload

        if use_case == "expansion":
            expansion_payload = self._run_expansion_pipeline(payload)
            print(json.dumps(expansion_payload, indent=4, sort_keys=True))
            save_expansion_output(db, expansion_payload, agent_run_id)
            return expansion_payload
        
        if use_case == "qbr":
            qbr_payload = self._run_qbr_pipeline(payload)
            print(json.dumps(qbr_payload, indent=4, sort_keys=True))
            print(json_safe(qbr_payload))
            try:
                save_qbr_output(db, qbr_payload, agent_run_id)
            except Exception as e:
                print("save_qbr_output failed:", e)
            return qbr_payload
        
        # in LLMOrchestrator.run_pipeline
        if use_case == "quality_incident":
            quality_payload = self._run_quality_pipeline(db, payload)
            print(json.dumps(quality_payload, indent=4, sort_keys=True))
            print(json_safe(quality_payload))
            save_quality_output(db, quality_payload, agent_run_id)
            return quality_payload

        if use_case == "supply_risk":
            supply_delay_payload = self._run_supply_risk_pipeline(payload)
            print(json.dumps(supply_delay_payload, indent=4, sort_keys=True))
            print(json_safe(supply_delay_payload))
            try:
                save_supply_output(db, supply_delay_payload, agent_run_id, payload["account"]["account_id"])
            except Exception as e:
                print("save_supply_output failed:", e)
            return supply_delay_payload

        raise ValueError(f"Unsupported use_case: {use_case}")


    def _run_churn_pipeline(self, payload: dict, account_name: str = "Customer"):
        self._initialize_chains()
        print("=== DEBUG: Starting pipeline ===")
        print(f"Payload: {json.dumps(payload, indent=2)}")

        account_id = payload.get("account", {}).get("account_id")
        if not account_id:
            raise ValueError("quality_incident pipeline requires payload.account.account_id")
    
        # RAG retrieval
        rag_docs = query_docs(
            query="""
            churn risk retention renewal downgrade usage drop adoption decline
            inactivity complaints support tickets SLA breach cancellation intent
            """,
            k=50,
            use_case="churn",
        )
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found: {len(rag_docs)}")
        print(f"RAG text preview: {rag_text[:200]}...")

        # Step 1: RCA
        print("=== Step 1: RCA ===")
        rca = self.rca_chain.invoke(
            {
                "context": json.dumps(payload),
                "rag": rag_text,
            }
        )
        print(f"RCA raw output type: {type(rca)}")
        print(f"RCA raw output: {rca}")

        # Step 2: Brief
        print("=== Step 2: Brief ===")
        brief = self.brief_chain.invoke(
            {
                "rca": json_safe(rca),
                "account_name": account_name,
            }
        )
        print(f"Brief raw output type: {type(brief)}")
        print(f"Brief raw output: {brief}")

        # Step 3: Actions
        print("=== Step 3: Actions ===")
        action = self.action_chain.invoke(
            {
                "brief": json_safe(brief),
            }
        )
        print(f"Actions raw output type: {type(action)}")
        print(f"Actions raw output: {action}")

        # Step 4: Email
        print("=== Step 4: Email ===")
        email = self.email_chain.invoke(
            {
                "brief": json_safe(brief),
            }
        )
        print(f"Email raw output type: {type(email)}")
        print(f"Email raw output: {email}")

        result = {
            "rca": rca or {},
            "brief": brief or {},
            "actions": action or {},
            "email": email or {},
        }

        return result


    def _run_expansion_pipeline(self, payload: dict):
        self._init_expansion_chains()

        print("=== EXPANSION PIPELINE STARTED ===")

        account_id = payload.get("account", {}).get("account_id")
        if not account_id:
            raise ValueError("quality_incident pipeline requires payload.account.account_id")

        rag_docs = query_docs(
    query="""
    expansion cross-sell upsell BOM adjacency competitor SKU wallet share 
    pricing playbook case study commercial expansion revenue margin
    """,
    k=50,
    use_case="expansion"
)   
        print("**********")
        print(payload)
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found: {len(rag_docs)}")
        print(f"RAG text preview: {rag_text[:200]}...")

        rca_chain = build_expansion_rca_chain(self.llm)
        prompt_inputs = {
            "context": json_safe(payload),
            "rag": rag_text
        }
        rca = rca_chain.invoke(prompt_inputs)
        print(f"RCA raw output type: {type(rca)}")
        print(f"RCA raw output: {rca}")

        print("brief call")
        breif_chain = build_expansion_brief_chain(self.llm)
        prompt_inputs = {
            "rca": json_safe(rca)
        }
        brief = breif_chain.invoke(prompt_inputs)
        print(f"brief raw output type: {type(brief)}")
        print(f"brief raw output: {brief}")


        print("revenue call")
        revenue_chain = build_expansion_revenue_chain(self.llm)
        prompt_inputs = {
            "rca": json_safe(rca),
            "brief": json_safe(brief)
        }
        revenue = revenue_chain.invoke(prompt_inputs)
        print(f"revaction_chainenue raw output type: {type(revenue)}")
        print(f"revenue raw output: {revenue}")


        print("actions call")
        action_chain = build_expansion_action_chain(self.llm)
        prompt_inputs = {
            "rca": json_safe(rca),
            "brief": json_safe(brief),
            "revenue": json_safe(revenue)
        }
        actions = action_chain.invoke(prompt_inputs)
        print(f"actions raw output type: {type(actions)}")
        print(f"actions raw output: {actions}")


        print("deck call")
        deck_chain = build_expansion_deck_chain(self.llm)
        prompt_inputs = {
            "brief": json_safe(brief)
        }
        deck = deck_chain.invoke(prompt_inputs)
        print(f"deck raw output type: {type(deck)}")
        print(f"deck raw output: {deck}")


        return {
            "use_case": "expansion",
            "rca": rca,
            "brief": brief,
            "revenue": revenue,
            "actions": actions,
            "deck": deck,
            "account_id": account_id
        }
    
    def _run_qbr_pipeline(self, payload: dict):
        """
        QBR pipeline: RCA -> Brief -> Opportunities -> Actions -> Deck -> Talking Points
        """
        self._init_qbr_chains()

        print("=== QBR PIPELINE STARTED ===")

        account_id = payload.get("account", {}).get("account_id")
        if not account_id:
            raise ValueError("quality_incident pipeline requires payload.account.account_id")
        
        # RAG retrieval scoped to qbr docs for this account
        account_name = payload.get("account", {}).get("account_name") or payload.get("account_name") or ""
        rag_docs = query_docs(account_name, k=50, use_case="qbr")
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found for QBR: {len(rag_docs)}")
        print(f"RAG preview: {rag_text[:200]}...")

        # Step 1: RCA
        rca_inputs = {
            "context": json_safe(payload),
            "rag": rag_text
        }
        rca_raw = self.qbr_rca_chain.invoke(rca_inputs)
        rca = parse_json_safe(rca_raw)
        print("RCA:", json_safe(rca))

        # Step 2: Brief
        brief_inputs = {"rca": json_safe(rca)}
        brief_raw = self.qbr_brief_chain.invoke(brief_inputs)
        brief = parse_json_safe(brief_raw)
        print("BRIEF:", json_safe(brief))

        # Step 3: Opportunities
        opp_inputs = {"rca": json_safe(rca), "brief": json_safe(brief)}
        opp_raw = self.qbr_opportunity_chain.invoke(opp_inputs)
        opportunities = parse_json_safe(opp_raw)
        print("OPPORTUNITIES:", json_safe(opportunities))

        # Step 4: Actions
        action_inputs = {"brief": json_safe(brief), "opportunities": json_safe(opportunities)}
        actions_raw = self.qbr_action_chain.invoke(action_inputs)
        actions = parse_json_safe(actions_raw)
        print("ACTIONS:", json_safe(actions))

        # Step 5: Deck
        deck_inputs = {"brief": json_safe(brief), "rca": json_safe(rca), "opportunities": json_safe(opportunities), "account_name": account_name}
        deck_raw = self.qbr_deck_chain.invoke(deck_inputs)
        deck = parse_json_safe(deck_raw)
        print("DECK:", json_safe(deck))

        # Step 6: Talking points
        talk_inputs = {"brief": json_safe(brief), "deck": json_safe(deck)}
        talk_raw = self.qbr_talk_chain.invoke(talk_inputs)
        talking_points = parse_json_safe(talk_raw)
        print("TALKING_POINTS:", json_safe(talking_points))

        return {
            "use_case": "qbr",
            "account_id": account_id,
            "rca": rca,
            "brief": brief,
            "opportunities": opportunities,
            "actions": actions,
            "deck": deck,
            "talking_points": talking_points
        }
    
    def _run_quality_pipeline(self, db, payload: dict):
        """
        Quality pipeline: Fetch incidents -> RCA -> Brief -> Actions -> Email
        """
        # Lazy init all quality chains
        self._init_quality_chains()

        print("=== QUALITY PIPELINE STARTED ===")

        # ----------------------------------------------------------------------
        # 1) FETCH INCIDENT DATA AGAIN FROM DB (last 30 days)
        # ----------------------------------------------------------------------
        account_id = payload.get("account", {}).get("account_id")
        if not account_id:
            raise ValueError("quality_incident pipeline requires payload.account.account_id")

        cutoff = datetime.utcnow().date() - timedelta(days=30)

        incidents = (
            db.query(QualityIncidents)
            .filter(
                QualityIncidents.account_id == account_id,
                QualityIncidents.incident_date >= cutoff
            )
            .order_by(QualityIncidents.incident_date.desc())
            .all()
        )

        incident_rows = []
        for inc in incidents:
            incident_rows.append({
                "incident_id": str(inc.incident_id),
                "incident_date": inc.incident_date.isoformat(),
                "defect_type": inc.defect_type,
                "severity": inc.severity,
                "resolution_status": inc.resolution_status,
                "line": inc.production_line,
                "shift": inc.shift,
                "supplier": inc.supplier_name,
                "supplier_lot": inc.supplier_lot,
                "material_batch": inc.material_batch,
                "description": inc.description,
            })

        print(f"Fetched {len(incident_rows)} incidents from DB for RCA")

        # ----------------------------------------------------------------------
        # 2) RAG RETRIEVAL
        # ----------------------------------------------------------------------
        account_name = payload.get("account", {}).get("account_name") or ""
        rag_docs = query_docs(account_name, k=50, use_case="quality_incident")
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found: {len(rag_docs)}")

        # ----------------------------------------------------------------------
        # 3) RCA
        # ----------------------------------------------------------------------
        rca_inputs = {
            "context": json_safe({
                "signal_payload": payload,
                "incident_data": incident_rows
            }),
            "rag": rag_text
        }

        rca_raw = self.quality_rca_chain.invoke(rca_inputs)
        rca = parse_json_safe(rca_raw)
        print("RCA parsed")
        print("RCA:", json_safe(rca))

        # ----------------------------------------------------------------------
        # 4) BRIEF
        # ----------------------------------------------------------------------
        brief_inputs = {"rca": json_safe(rca)}
        brief_raw = self.quality_brief_chain.invoke(brief_inputs)
        brief = parse_json_safe(brief_raw)
        print("BRIEF parsed")
        print("BRIEF:", json_safe(brief))


        # ----------------------------------------------------------------------
        # 5) ACTIONS
        # ----------------------------------------------------------------------
        action_inputs = {"brief": json_safe(brief), "rca": json_safe(rca)}
        actions_raw = self.quality_action_chain.invoke(action_inputs)
        actions = parse_json_safe(actions_raw)
        print("ACTIONS parsed")
        print("ACTIONS:", json_safe(actions))

        # ----------------------------------------------------------------------
        # 6) EMAIL
        # ----------------------------------------------------------------------
        email_inputs = {"brief": json_safe(brief), "actions": json_safe(actions)}
        email_raw = self.quality_email_chain.invoke(email_inputs)
        email = parse_json_safe(email_raw)
        print("EMAIL parsed")
        print("EMAIL:", json_safe(email))


        # ----------------------------------------------------------------------
        # 7) FINAL ASSEMBLED OUTPUT
        # ----------------------------------------------------------------------
        result = {
            "account_id": account_id,
            "use_case": "quality_incident",
            "rca": rca,
            "brief": brief,
            "actions": actions,
            "email": email
        }
        return result

    def _run_supply_risk_pipeline(self, payload: dict):
        self._init_supply_risk_chains()

        print("=== SUPPLY DELAY PIPELINE STARTED ===")

        rag_docs = query_docs(
    query="""
        supply delay late shipment missed SLA raw material shortage inventory coverage 
        PO delay ASN overdue ETA variance line stoppage backorder risk expediting 
        reroute supplier alternate carrier air freight credit advance mitigation playbook
        """,
    k=50,
    use_case="supply_risk"
)
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found: {len(rag_docs)}")
        print(f"RAG text preview: {rag_text[:200]}...")
        # Step 1: RCA
        print("=== Step 1: RCA ===")
        rca_chain = build_supply_rca_chain(self.llm)
        prompt_inputs = {
            "context": json_safe(payload),
            "rag": rag_text
        }
        rca = rca_chain.invoke(prompt_inputs)
        print(f"RCA raw output type: {type(rca)}")
        print(f"RCA raw output: {rca}")
        # Step 2: Brief
        print("=== Step 2: Brief ===")
        brief_chain = build_supply_brief_chain(self.llm)
        prompt_inputs = {
            "rca": json_safe(rca)
        }
        brief = brief_chain.invoke(prompt_inputs)
        print(f"BRIEF raw output type: {type(brief)}")
        print(f"BRIEF raw output: {brief}")
        # Step 3: Actions
        print("=== Step 3: Actions ===")
        action_chain = build_supply_action_chain(self.llm)
        prompt_inputs = {
            "brief": json_safe(brief)
        }
        actions = action_chain.invoke(prompt_inputs)
        print(f"ACTIONS raw output type: {type(actions)}")
        print(f"ACTIONS raw output: {actions}")
        # Step 4: Email
        print("=== Step 4: Email ===")
        email_chain = build_supply_email_chain(self.llm)
        prompt_inputs = {
            "brief": json_safe(brief)
        }
        email = email_chain.invoke(prompt_inputs)
        print(f"EMAIL raw output type: {type(email)}")
        print(f"EMAIL raw output: {email}")
        result = {
            "rca": rca or {},
            "brief": brief or {},
            "actions": actions or {},
            "email": email or {},
        }
        return result
