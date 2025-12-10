from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_expansion_revenue_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
You are a pricing and revenue analyst.
You MUST return ONLY valid JSON.
Do NOT include any explanation, headings, or notes.
Do NOT wrap JSON in backticks.
Do NOT add any text before or after the JSON.
Input data:
- Signals JSON: {rca}
- Business context: {brief}

Estimate revenue opportunity.

Return ONLY JSON:
{{
  "revenue_model": [
    {{
      "sku": "SKU",
      "current_monthly_qty": 0,
      "target_monthly_qty": 0,
      "unit_price": 0,
      "estimated_monthly_revenue": 0
    }}
  ],
  "total_estimated_monthly_revenue": 0,
  "assumptions": [
    "List of explicit commercial assumptions"
  ]
}}

NO SALES LANGUAGE. NO STRATEGY.
""")

    return prompt | llm | JsonOutputParser()
