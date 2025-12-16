# backend/llm/quality_chains/action_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_quality_action_chain(llm):
    """
    Input: {"brief": <json-stringified brief>, "rca": <json-stringified rca>}
    Returns actions JSON similar to your QBR action_chain format.
    """
    prompt = ChatPromptTemplate.from_template(r"""
You are a CRM assistant that generates actionable tasks for the KAM and operations team.

You MUST return ONLY valid JSON.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null                                                 

Brief:
{brief}

RCA:
{rca}

Return JSON:
{{
  "actions": [
    {{
      "title": "Short title",
      "description": "Detailed description of the action",
      "priority": "High/Medium/Low",
      "type": "replacement/audit/meeting/email/task",
      "assignee_suggestion": "role or name",
      "expected_impact": {{"reduction_in_defects_percent": 0.0}}
    }}
  ]
}}
""")
    return prompt | llm | JsonOutputParser()
