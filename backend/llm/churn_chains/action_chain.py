from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_action_chain(llm):
    """
    Input variables expected:
      - brief: JSON string of the brief output
    """
    prompt = ChatPromptTemplate.from_template(
        r"""
You are an operations manager turning an executive brief into concrete actions.

Executive brief (JSON):
{brief}

Generate 3–7 specific operational actions.
Each action must clearly state:
- What to do
- Who owns it
- Priority
- Target due date (YYYY-MM-DD)

You MUST follow these rules:
- Return your answer as JSON ONLY.
- Do NOT write any introductions, explanations, or comments.
- Do NOT write phrases like "Here are the actions", "Here is the result", or similar.
- Do NOT use code fences.

Return EXACTLY one JSON object with this structure:

{{
  "actions": [
    {{
      "action": "Specific task to execute",
      "owner": "Team or role (e.g. CSM, Sales, Ops)",
      "priority": "High/Medium/Low",
      "due_date": "2025-12-31"
    }}
  ]
}}
"""
    )

    return prompt | llm | JsonOutputParser()

