from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_supply_rca_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        r"""
You are a supply chain risk analyst.
Perform ROOT CAUSE ANALYSIS only. Do NOT propose actions or solutions.

Given:
1) Payload (JSON):
{context}

2) RAG docs:
{rag}

Task:
- Identify the main root causes for supply risk (delivery delays, material shortages, customer impact).
- For each cause, estimate a confidence between 0 and 1.
- Provide an overall confidence_score for your analysis.
- Classify severity of supply risk and summarize business impact.

Return your answer as JSON ONLY.
Do not include any explanation, commentary, prefixes, or suffixes.

The JSON must have exactly this structure and field names.  Details are just for example:

{{
  "root_causes": [
    {{
      "cause": "specific reason (short sentence)",
      "confidence": 0.0-1.0,
      "category": "Delivery|Supply|Customer"
    }}
  ],
  "confidence_score": 0.0-1.0,
  "severity": "Critical" | "High" | "Medium" | "Low",
  "business_impact": "Short description of expected operational/revenue impact"
}}
"""
    )
    return prompt | llm | JsonOutputParser()
