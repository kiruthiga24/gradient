# backend/llm/quality_chains/rca_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_quality_rca_chain(llm):
    """
    Input to .invoke(): {"context": <json-string of payload>, "rag": <rag_text>}
    Returns parsed JSON (via JsonOutputParser).
    """
    prompt = ChatPromptTemplate.from_template(r"""
You are an expert manufacturing quality root-cause analyst.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null

Context (signal + lightweight context):
{context}

RAG supporting documents (relevant incident notes and metadata):
{rag}

Produce a JSON object with the following structure:
{{
  "correlated_factors": {{
    "shift": [{{"value": "A", "count": 5}}, ...],
    "line": [{{"value":"L1","count":4}}, ...],
    "supplier": [{{"value":"SuppCo","count":3}}, ...],
    "supplier_lot": [{{"value":"LOT-123","count":2}}, ...],
    "material_batch": [{{"value":"BATCH-1","count":2}}, ...]
  }},
  "trends": {{
    "daily_counts": [{{"date":"2025-12-01","count":2}}, ...],
    "recent_vs_baseline": {{"recent": 6, "baseline": 2, "ratio": 3.0}}
  }},
  "defect_patterns": [
    {{"defect_code":"D123","count":5,"severity":"High"}},
    ...
  ],
  "hypothesis": "A short 1-3 sentence hypothesis about root cause",
  "root_cause_summary": "5-7 sentence explanation synthesizing the evidence",
  "total_incidents": 12,
  "notes": "Optional short notes or null"
}}

Ensure output is strict JSON.
""")
    # json parser will ensure the chain returns JSON object
    return prompt | llm | JsonOutputParser()
