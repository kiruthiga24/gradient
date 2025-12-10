from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

def build_email_chain(llm):
    prompt = ChatPromptTemplate.from_template(
       
        template=r"""
Using this brief, generate an outreach email in JSON with this EXACT structure:

{{
  "subject": "Clear subject line",
  "body_text": "Professional email body"
}}

BRIEF:
{brief}

Output ONLY valid JSON. No additional text.
        """
    )
    
    chain = prompt | llm | JsonOutputParser()
    return chain
