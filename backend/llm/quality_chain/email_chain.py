# backend/llm/quality_chains/email_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_quality_email_chain(llm):
    """
    Input: {"brief": <json-stringified brief>, "actions": <json-stringified actions>}
    Returns JSON: {"subject": "...", "body": "..."}
    """
    prompt = ChatPromptTemplate.from_template(r"""
You are a helpful, empathetic customer-facing communicator.

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

Planned actions:
{actions}

Write an apology + recovery plan email draft for the KAM to send to the customer.
Return JSON:
{{
  "subject": "short subject <80 chars",
  "body": "email body ~200-300 words"
}}
""")
    return prompt | llm | JsonOutputParser()
