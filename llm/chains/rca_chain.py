from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_rca_chain(llm):
    prompt = ChatPromptTemplate.from_template(r"""
Analyze account data. IDENTIFY ROOT CAUSES ONLY. NO recommendations/actions.

Context: {context}
RAG Docs: {rag}

Return ONLY JSON:
{{
  "root_causes": [
    {{"cause": "Specific root cause", "confidence": 0.9}}
  ],
  "severity": "Critical/High/Medium",
  "business_impact": "Revenue/customers at risk"
}}

DIAGNOSE ONLY. No solutions.
    """)
    return prompt | llm | JsonOutputParser()