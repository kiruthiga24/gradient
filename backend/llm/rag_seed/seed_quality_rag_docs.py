# backend/llm/rag_seed/seed_quality_rag_docs.py
from rag_store import add_documents  # adapt import to your rag_store helper
import json

docs = [
    ("Quality_Root_Cause_Playbook", "When a defect spike occurs, check supplier lots, production line config, and recent change orders. Prioritize stops on lines with repeated defects."),
    ("Quality_Audit_Checklist", "Checklist: containment, sorting, root cause sampling, supplier quarantine, replacement plan, customer communication."),
    ("Quality_COPQ_Impact", "COPQ calculation method and example templates for estimating cost of poor quality."),
]

documents = [content for (_, content) in docs]
metadatas = [{"title": title, "use_case": "quality_incident"} for (title, _) in docs]

print(f"Adding {len(documents)} quality docs to ChromaDB…")
add_documents(documents, metadatas)
print("RAG seeding complete.")
