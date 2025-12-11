from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_supply_action_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        r"""
You are a supply chain operations lead.
Generate ACTION PLAN only. NO ANALYSIS. DO NOT add extra text, explanations, or notes.

Given brief:
{brief}

Task:
- List 3-5 prioritized actions (expedite, reroute, credit, etc.)
- Assign owners and timelines
- Define success criteria

Return EXACTLY this JSON format (no extra text, no markdown). The details below are **structure only**, not actual values:

{{
  "immediate_actions": [
    {{"action": "<string>", "owner": "<string>", "due": "<string>"}}
  ],
  "followup_actions": [
    {{"action": "<string>", "owner": "<string>", "due": "<string>"}}
  ],
  "owners": ["<string>"],
  "timeline": "<string>",
  "success_criteria": ["<string>"]
}}
"""
    )
    return prompt | llm | JsonOutputParser()
