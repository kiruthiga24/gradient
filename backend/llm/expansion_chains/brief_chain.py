from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_expansion_brief_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are a commercial strategy analyst.

Transform raw expansion signals into BUSINESS EXPLANATION ONLY.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
Input RCA JSON:
{rca}

Return ONLY JSON:
{{
  "executive_summary": "Short business-friendly explanation",
  "commercial_insight": "Why this matters from revenue perspective",
  "detected_patterns": [
    {{"pattern": "Description", "impact": "Revenue / volume impact"}}
  ],
  "revenue_upside_summary": "Plain English estimate"
}}

NO ACTIONS. NO RECOMMENDATIONS.
""")

    return prompt | llm | JsonOutputParser()
