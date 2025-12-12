from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

def build_email_chain(llm):
    """
    Input variables expected:
      - brief: JSON string of the brief output
    """
    prompt = ChatPromptTemplate.from_template(
        r"""
You are a customer success manager writing an outreach email to the client,
based on the executive brief.

Executive brief (JSON):
{brief}

Write a clear, empathetic email that:
- Acknowledges the issues
- Summarizes the situation in simple language
- Proposes next steps or a call
- Stays professional and concise

Return your answer as JSON ONLY.
Do not include any explanation, commentary, prefixes, or suffixes.

The JSON must have exactly this structure:

{{
  "subject": "Short, clear subject line about churn risk / partnership health",
  "body_text": "Full email body in plain text with line breaks."
}}
"""
    )

    
    chain = prompt | llm | JsonOutputParser()
    return chain
