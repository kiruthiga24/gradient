# llm/chains/qbr_chains.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# RCA: analyze account metrics and produce structured JSON signals
def build_qbr_rca_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are an analyst.  Analyze the account quarterly metrics and IDENTIFY ROOT CAUSES and SIGNALS ONLY.
Do NOT provide recommendations.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null
                                                                                          
Context: {context}
RAG Docs: {rag}

Return ONLY JSON with structure:
{{
  "trends": {{"orders": "...", "usage": "...", "quality": "...", "tickets": "..."}},
  "root_causes": [{{"issue":"text","confidence":0.0}}],
  "signals": {{"wins": [], "risks": [], "opportunities": []}},
  "kpi_summary": {{"revenue": 0, "nps": 0}}
}}
""")
    return prompt | llm | JsonOutputParser()