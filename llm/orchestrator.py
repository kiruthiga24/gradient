import json
from llm_factory import get_llm
from rag_store import query_docs
from chains.rca_chain import build_rca_chain
from chains.brief_chain import build_brief_chain
from chains.action_chain import build_action_chain
from chains.email_chain import build_email_chain

class LLMOrchestrator:
    def __init__(self):
        self.llm = None
        self.rca_chain = None
        self.brief_chain = None
        self.action_chain = None
        self.email_chain = None
    
    def _initialize_chains(self):
        """Lazy initialization of chains"""
        if self.llm is None:
            self.llm = get_llm()
        
        if self.rca_chain is None:
            self.rca_chain = build_rca_chain(self.llm)
        if self.brief_chain is None:
            self.brief_chain = build_brief_chain(self.llm)
        if self.action_chain is None:
            self.action_chain = build_action_chain(self.llm)
        if self.email_chain is None:
            self.email_chain = build_email_chain(self.llm)
    
    def run_pipeline(self, payload):
    
        self._initialize_chains()
        print("=== DEBUG: Starting pipeline ===")
        print(f"Payload: {json.dumps(payload, indent=2)}")
    
        # RAG retrieval
        rag_docs = query_docs(payload.get("account_name", ""))
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
