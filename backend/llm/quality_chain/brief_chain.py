# backend/llm/quality_chains/brief_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_quality_brief_chain(llm):
    """
    Input: {"rca": <json-stringified rca>}
    Returns JSON: {"executive_summary": "...", "action_plan": ["step1","step2","step3"], ...}
    """
    prompt = ChatPromptTemplate.from_template(r"""
You are a senior manufacturing account lead writing an executive-ready Quality Incident Summary.

You MUST return ONLY valid JSON.
Do not add any text outside JSON.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null   
                                              
Root Cause Summary:
{rca}

Produce JSON with:
{{
  "executive_summary": "6-8 sentence executive summary (empathic + factual)",
  "key_findings": ["finding 1", "finding 2"],
  "risk_level": "High/Medium/Low",
  "impact_estimate": 0.0,
  "action_plan": ["Step 1", "Step 2", "Step 3"]
}}
""")
    return prompt | llm | JsonOutputParser()
