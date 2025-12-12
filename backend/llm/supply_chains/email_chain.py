from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_supply_email_chain(llm):
    prompt = ChatPromptTemplate.from_template(
        r"""You are a customer success manager.

Given the brief: {brief}

Draft a customer email in JSON format ONLY, using these fields:

{{
  "subject": "string",
  "body": "string",
  "recipients": ["string"],
  "priority": "Normal | High | Urgent",
  "cc": ["string"]
}}

JSON ONLY. Do not include any explanation, notes, or extra text.
""" )
    return prompt | llm | JsonOutputParser()
