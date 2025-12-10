import json, uuid
from .rag_seed.rag_store import query_docs

from .llm_factory import get_llm
from .save_to_db import save_expansion_output

from .chains.rca_chain import build_rca_chain
from .chains.brief_chain import build_brief_chain
from .chains.action_chain import build_action_chain
from .chains.email_chain import build_email_chain

from .expansion_chains.action_chain import build_expansion_action_chain
from .expansion_chains.brief_chain import build_expansion_brief_chain
from .expansion_chains.deck_chain import build_expansion_deck_chain
from .expansion_chains.rca_chain import build_expansion_rca_chain
from .expansion_chains.revenue_chain import build_expansion_revenue_chain
import json
from decimal import Decimal

def json_safe(obj):
    """
    Converts Decimal to float for JSON serialization
    """
    return json.dumps(obj, default=lambda x: float(x) if isinstance(x, Decimal) else x)


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
    
    # ----------------------------
    # Entry point
    # ----------------------------
    def run_pipeline(self, db, use_case: str, payload: dict, agent_run_id: uuid):
        """
        use_case:
          - "churn"
          - "expansion"
        """
        if use_case == "churn":
            return self._run_churn_pipeline(payload)

        if use_case == "expansion":
            expansion_payload = self._run_expansion_pipeline(payload)
            print(json.dumps(expansion_payload, indent=4, sort_keys=True))
            save_expansion_output(db, expansion_payload, agent_run_id)
            return expansion_payload

        raise ValueError(f"Unsupported use_case: {use_case}")

    
    def _run_churn_pipeline(self, payload):
    
        self._initialize_chains()
        print("=== DEBUG: Starting pipeline ===")
        print(f"Payload: {json.dumps(payload, indent=2)}")
    
        # RAG retrieval
        rag_docs = query_docs(payload.get("account_name", ""), use_case="churn")
        rag_text = "\n\n".join([d["text"] for d in rag_docs])
        print(f"RAG docs found: {len(rag_docs)}")
        print(f"RAG text preview: {rag_text[:200]}...")
        
        print("=== Step 1: RCA ===")
        # Step 1: RCA - FIXED: .invoke() with dict input
        rca_raw = self.rca_chain.invoke({
            "context": json.dumps(payload), 
            "rag": rag_text
        })
        print(f"RCA raw output type: {type(rca_raw)}")
        print(f"RCA raw output: {rca_raw}")
        # rca, _ = parse_json_safe(rca_raw)
        # print(f"RCA parsed: {rca}")
        # print(f"Parse error: {_}")
        
        # Step 2: Brief - FIXED
        print("=== Step 2: Brief ===")
        brief_raw = self.brief_chain.invoke({"rca": json.dumps(rca_raw),"account_name": payload.get("account_name")}) or {}
        print(f"Brief raw: {brief_raw}")
        # brief, _ = parse_json_safe(brief_raw)
        # print(f"Brief parsed: {brief}")

        # Step 3: Actions - FIXED
        print("=== Step 3: Actions ===")
        actions_raw = self.action_chain.invoke({"brief": json.dumps(brief_raw)})
        print(f"Actions raw: {actions_raw}")
        # actions, _ = parse_json_safe(actions_raw)
        # print(f"Actions parsed: {actions}")
        
        # Step 4: Email - FIXED
        print("=== Step 4: Email ===")
        email_raw = self.email_chain.invoke({"brief": json.dumps(brief_raw)})
        print(f"Email raw: {email_raw}")

        # print(f"Email parsed: {email}")

        result = {
            "rca": rca_raw or {},
            "brief": brief_raw or {},
            "actions": actions_raw or {},
            "email": email_raw or {}
        }
        print(f"Final result: {json.dumps(result, indent=2)}")
        return result


    def _run_expansion_pipeline(self, payload: dict):
        self._init_expansion_chains()

        print("=== EXPANSION PIPELINE STARTED ===")

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
            "deck": deck
        }