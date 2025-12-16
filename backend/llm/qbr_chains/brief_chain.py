from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Brief: executive summary and narrative for middle panel
def build_qbr_brief_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are a senior account executive. Given the RCA JSON below, craft an executive brief for a QBR.

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null
                                              
RCA: {rca}

Return ONLY JSON:
{{
  "executive_summary": "string",
  "key_wins": ["..."],
  "key_risks": ["..."],
  "opportunities_summary": ["..."]
}}

""")
    return prompt | llm | JsonOutputParser()
