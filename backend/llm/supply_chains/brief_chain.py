from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_supply_brief_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        r"""
You are a supply chain executive briefer.

Input RCA: {rca}

OUTPUT JSON ONLY. NO OTHER TEXT.

{{
  "situation": "1 sentence summary",
  "priority": "Monitor|Escalate|Immediate", 
  "urgency_score": 1-10,
  "key_metrics": {{
    "primary_risk": "str",
    "revenue_impact": "str"
  }}
}}
"""
    )
    return prompt | llm | JsonOutputParser()