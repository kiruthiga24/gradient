from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_expansion_action_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are a Key Account Manager assistant.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null   
                                                                                            
Input:
- RCA JSON: {rca}
- Brief JSON: {brief}
- Revenue JSON: {revenue}

Generate NEXT BEST ACTIONS.

Return ONLY JSON:
{{
  "actions": [
    {{
      "action_type": "meeting/email/deck/quote/task",
      "title": "Short action label",
      "description": "Clear step for KAM",
      "priority": "High/Medium/Low"
    }}
  ]
}}

FOCUS ONLY ON EXECUTABLE ACTIONS.
""")

    return prompt | llm | JsonOutputParser()
