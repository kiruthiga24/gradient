# llm/rag_seed_qbr.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_store import add_documents

docs = [
    ("QBR_Template_Guidelines",
     """Quarterly Business Reviews should include: Executive summary, trends, wins, risks, opportunities, savings, and action plan.
Use 3-5 slides for executive summary and 5-8 slides total for a standard QBR. Include KPIs, trend charts, and a one-slide recommended action plan."""),

    ("QBR_Storytelling_BestPractices",
     """Tell the story: start with outcome (executive summary), show evidence (trends + data), show impact (revenue/cost), recommend actions. Keep slides concise and quantifiable."""),

    ("QBR_Manufacturing_Case_Study",
     """Case: Customer X QBR — highlighted a production bottleneck causing a 12% drop in on-time shipment. Action: prioritized maintenance schedule and added buffer stock; lost revenue recovered."""),

    ("QBR_Talking_Points_Template",
     """Talking points: 1) What went well 2) Root causes of issues 3) Quantified impact 4) Proposed ask and next steps. Always include one clear 'ask' for the customer (e.g., trial of new SKU).""")
]

documents = [content for (_, content) in docs]
metadatas = [{"title": title, "use_case": "qbr"} for (title, _) in docs]

print(f"Adding {len(documents)} QBR docs to ChromaDB…")
add_documents(documents, metadatas)
print("RAG seeding complete.")
