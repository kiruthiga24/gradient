from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_action_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
From the executive brief, CREATE NEW operational tasks. 

IMPORTANT:
- Output STRICT JSON ONLY.
- Do NOT write Markdown, bullet points, explanations, or numbered lists.
- Do NOT copy root causes; generate FRESH operational actions.

Brief: {brief}

Output format EXACTLY like this:
[
  {{"action": "WHO does WHAT by WHEN", "owner": "marketing/ops/sales", "priority": "High/Medium", "due": "YYYY-MM-DD"}}
]

Return ONLY valid JSON.
""")
    return prompt | llm | JsonOutputParser()

