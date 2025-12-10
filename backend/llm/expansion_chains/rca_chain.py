from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_expansion_rca_chain(llm):
    print("expansion rca chain")
    prompt = ChatPromptTemplate.from_template(r"""
Analyze SKU usage patterns. IDENTIFY EXPANSION SIGNALS ONLY. NO recommendations.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.

Context: {context}
RAG Docs: {rag}

Return ONLY JSON:
{{
  "usage_anomalies": [
    {{"sku": "SKU_NAME", "pattern": "Overconsumption pattern", "confidence": 0.0}}
  ],
  "competitor_dependency": [
    {{"our_sku": "SKU", "their_sku": "SKU", "evidence": "text"}}
  ],
  "bom_gaps": [
    {{"missing_sku": "SKU", "linked_sku": "SKU", "reason": "BOM mismatch"}}
  ],
  "revenue_leakage_estimate": {{
    "monthly_value": 0,
    "currency": "USD"
  }}
}}

NO SUGGESTIONS. NO ACTIONS. ONLY SIGNALS.
""")

    return prompt | llm | JsonOutputParser()
