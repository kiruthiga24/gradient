from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_rca_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        r"""
You are a B2B customer success analyst.
Perform ROOT CAUSE ANALYSIS only. Do NOT propose actions or solutions.

Given:

1) Payload (JSON):
{context}

2) RAG docs:
{rag}

Task:
- Identify the main root causes for churn risk for this account.
- For each cause, estimate a confidence between 0 and 1.
- Provide an overall confidence_score for your analysis.
- Classify severity of churn risk and summarize business impact.

Return your answer as JSON ONLY.
Do not include any explanation, commentary, prefixes, or suffixes.
Do not include phrases like "Here is the result" or code fences.

The JSON must have exactly this structure and field names:

{{
  "root_causes": [
    {{
      "cause": "specific reason (short sentence)",
      "confidence": 0.0-1.0
    }}
  ],
  "confidence_score": 0.0-1.0,
  "severity": "Critical" | "High" | "Medium" | "Low",
  "business_impact": "Short description of expected revenue/customer impact"
}}
"""
    )

    return prompt | llm | JsonOutputParser()