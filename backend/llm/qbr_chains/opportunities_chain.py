from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Opportunities: produce concrete sku/opportunity list with estimated value
def build_qbr_opportunity_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Given RCA and brief, list concrete opportunities (upsell, cross-sell, whitespace).

You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
- Use decimal numbers only, no fractions
- Replace any unknown value with 0 or null
- Do not use Python None; use JSON null
                                              
RCA: {rca}
Brief: {brief}

Return ONLY JSON:
{{
  "opportunities": [
    {{"type":"upsell/cross-sell/whitespace","sku":"SKU","rationale":"...","estimated_value":0}}
  ]
}}

""")
    return prompt | llm | JsonOutputParser()