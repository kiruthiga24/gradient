from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Actions: CRM action items for KAM to drive
def build_qbr_action_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are a CRM assistant.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null                                              

Brief: {brief}
Opportunities: {opportunities}

Generate CRM tasks with title, description, priority, type, and assignee_suggestion.

Return ONLY JSON:
{{
  "actions": [
    {{
      "title": "...",
      "description": "...",
      "priority": "High/Medium/Low",
      "type": "meeting/email/task",
      "assignee_suggestion": "role or name"
    }}
  ]
}}

""")
    return prompt | llm | JsonOutputParser()
